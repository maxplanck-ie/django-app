from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from common.utils import get_form_errors
from request.models import Request, RequestForm, FileDeepSeqRequest
from library.models import Library, Sample

import json
from datetime import datetime
import logging

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.rl_config import defaultPageSize

logger = logging.getLogger('db')
User = get_user_model()


@login_required
def get_requests(request):
    """ Get the list of all requests and send it to frontend """
    error = str()
    data = []

    try:
        if request.user.is_staff:
            requests = Request.objects.select_related()
        else:
            requests = Request.objects.filter(
                researcher_id=request.user.id
            ).select_related()

        data = [
            {
                'requestId': req.id,
                'status': req.status,
                'name': req.name,
                'dateCreated': req.date_created.strftime('%d.%m.%Y'),
                'description': req.description,
                'researcherId': req.researcher.id,
                'researcher': req.researcher.name,
                'deepSeqRequestName':
                    req.deep_seq_request.name
                    if req.deep_seq_request is not None else '',
                'deepSeqRequestPath':
                    settings.MEDIA_URL + req.deep_seq_request.file.name
                    if req.deep_seq_request is not None else '',
                'sumSeqDepth': sum([
                    l.sequencing_depth
                    for l in list(req.libraries.all())+list(req.samples.all())
                ])
            }
            for req in requests
        ]
        data = sorted(data, key=lambda x: x['status'])

    except Exception as e:
        error = str(e)
        print('[ERROR]: get_requests/: %s' % error)
        logger.debug(error)

    return HttpResponse(
        json.dumps({
            'success': not error,
            'error': error,
            'data': sorted(
                data,
                key=lambda x: x['requestId'],
                reverse=True,
            )
        }),
        content_type='application/json',
    )


@login_required
def save_request(request):
    """ Add new or edit an existing request """
    error = str()
    mode = request.POST.get('mode')

    try:
        if request.method == 'POST':
            if mode == 'add':
                form = RequestForm(request.POST)
            elif mode == 'edit':
                request_id = request.POST.get('request_id')
                req = Request.objects.get(id=request_id)
                form = RequestForm(request.POST, instance=req)

            if form.is_valid():
                if mode == 'add':
                    req = form.save(commit=False)
                    # Set initial values
                    req.status = 0
                    req.researcher = User.objects.get(id=request.user.id)
                    req.save()
                    req.name = 'Request' + str(req.id)  # ensure uniqueness
                    req.save()
                else:
                    req = form.save()
                libraries = json.loads(request.POST.get('libraries'))
                samples = json.loads(request.POST.get('samples'))

                request_libraries = Library.objects.filter(id__in=libraries)
                for library in request_libraries:
                    library.is_in_request = True
                    library.save()
                req.libraries.add(*libraries)

                request_samples = Sample.objects.filter(id__in=samples)
                for sample in request_samples:
                    sample.is_in_request = True
                    sample.save()
                req.samples.add(*samples)

            else:
                raise Exception(get_form_errors(form.errors))

    except Exception as e:
        error = str(e)
        print('[ERROR]: edit_request/: %s' % error)
        logger.debug(error)

    return HttpResponse(
        json.dumps({
            'success': not error,
            'error': error,
        }),
        content_type='application/json',
    )


@login_required
def delete_request(request):
    error = str()

    try:
        request_id = int(request.POST.get('request_id'))
        req = Request.objects.get(id=request_id)
        libraries_samples = list(req.libraries.all()) + list(req.samples.all())
        for obj in libraries_samples:
            obj.delete()
        req.delete()

    except Exception as e:
        error = str(e)
        print('[ERROR]: delete_request/: %s' % error)
        logger.debug(error)

    return HttpResponse(
        json.dumps({
            'success': not error,
            'error': error,
        }),
        content_type='application/json',
    )


@login_required
def get_libraries_in_request(request):
    """ """
    error = ''
    data = []

    try:
        request_id = request.GET.get('request_id')
        req = Request.objects.get(id=request_id)
        libraries = [
            {
                'name': library.name,
                'recordType': 'L',
                'libraryId': library.id,
                'barcode': library.barcode,
            }
            for library in req.libraries.all()
        ]
        samples = [
            {
                'name': sample.name,
                'recordType': 'S',
                'sampleId': sample.id,
                'barcode': sample.barcode,
            }
            for sample in req.samples.all()
        ]
        data = sorted(libraries+samples, key=lambda x: x['barcode'])

    except Exception as e:
        error = str(e)
        print('[ERROR]: get_libraries_in_request/: %s' % error)
        logger.debug(error)

    return HttpResponse(
        json.dumps({
            'success': not error,
            'error': error,
            'data': data,
        }),
        content_type='application/json',
    )


# Helper functions

def draw_page_header(p, font, font_size):
    """ """
    page_width = defaultPageSize[0]
    page_height = defaultPageSize[1]
    title = 'Deep Sequencing Request'
    p.setFont(font, font_size)
    p.drawCentredString(page_width/2.0, page_height-75, title)


def draw_string(p, x, _x, y, font, font_bold, font_size, label, string):
    """ """
    p.setFont(font_bold, font_size)
    p.drawString(x, y, label)
    p.setFont(font, font_size)
    p.drawString(_x, y, string)


def draw_table_row(p, x, y, string):
    """ """
    _x, _y = x, y
    _y -= 30
    p.drawString(_x, _y, string[0])
    _x += 25
    p.drawString(_x, _y, string[1])
    _x += 300
    p.drawString(_x, _y, string[2])
    _x += 70
    p.drawString(_x, _y, string[3])


@csrf_exempt
@login_required
def generate_pdf(request):
    """ """
    request_id = request.GET.get('request_id')
    response = HttpResponse(content_type='application/pdf')

    try:
        req = Request.objects.get(id=request_id)
        user = User.objects.get(id=req.researcher_id)
        cost_unit = sorted([u.name for u in user.cost_unit.all()])
        filename = req.name + '_Deep_Sequencing_Request.pdf'
        response['Content-Disposition'] = 'inline; filename="%s"' % filename

        p = canvas.Canvas(response)
        FONT_BOLD = 'Helvetica-Bold'
        FONT = 'Helvetica'
        HEADER_FONT_SIZE = 14
        DEFAULT_FONT_SIZE = 12
        SMALL_FONT_SIZE = 10
        LINE_SPACING = 20

        x = inch
        y = 10 * inch + 25

        # Strings
        request_name = req.name
        description = req.description
        submitted_libraries_samples = 'List of samples/libraries to be ' + \
            'submitted for sequencing:'
        page_1 = 'Page 1 of 2'
        page_2 = 'Page 2 of 2'

        # Page 1
        _x = x + 150
        _y = y - 10
        draw_page_header(p, FONT_BOLD, HEADER_FONT_SIZE)

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Request Name:', request_name,
        )
        _y -= LINE_SPACING

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Date:', datetime.now().strftime('%d.%m.%Y'),
        )
        _y -= LINE_SPACING

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Request Number:', '',
        )
        _y -= LINE_SPACING

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Provider:', '',
        )
        _y -= LINE_SPACING * 1.5

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'User:', user.name,
        )
        _y -= LINE_SPACING

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Phone:', user.phone,
        )
        _y -= LINE_SPACING

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Email:', user.email
        )
        _y -= LINE_SPACING

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Organization:', user.organization.name,
        )
        _y -= LINE_SPACING

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Principal Investigator:',
            user.pi.name if user.pi is not None else '',
        )
        _y -= LINE_SPACING

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Cost Unit(s):',
            ', '.join(cost_unit) if any(cost_unit) else '',
        )
        _y -= LINE_SPACING * 1.5

        draw_string(
            p, x, _x, _y, FONT, FONT_BOLD, DEFAULT_FONT_SIZE,
            'Description:', description,
        )
        _y -= LINE_SPACING

        # Signature
        signature_y = 1.5 * inch
        p.setFont(FONT, SMALL_FONT_SIZE-1)
        p.line(x, signature_y+10, x+125, signature_y+10)
        p.drawString(x+30, signature_y, '(Date, Signature)')
        p.line(x+150, signature_y+10, x+300, signature_y+10)
        p.drawString(x+180, signature_y, '(Principal Investigator)')

        p.setFont(FONT, SMALL_FONT_SIZE)
        p.drawString(x*6.5, inch, page_1)   # Page counter
        p.showPage()

        # Page 2
        _y = y - 10
        draw_page_header(p, FONT_BOLD, HEADER_FONT_SIZE)
        p.setFont(FONT_BOLD, DEFAULT_FONT_SIZE)
        p.drawString(x, _y, submitted_libraries_samples)
        p.setFont(FONT_BOLD, SMALL_FONT_SIZE)
        draw_table_row(p, x, y-10, ('#', 'Name', 'Type', 'Barcode'))
        p.setFont(FONT, SMALL_FONT_SIZE)

        libraries = [
            {
                'name': library.name,
                'type': 'Library',
                'barcode': library.barcode,
            }
            for library in req.libraries.all()
        ]
        samples = [
            {
                'name': sample.name,
                'type': 'Sample',
                'barcode': sample.barcode,
            }
            for sample in req.samples.all()
        ]
        data = sorted(libraries+samples, key=lambda x: x['barcode'])

        # Only ~55 records fit into the page
        for i, record in enumerate(data):
            draw_table_row(
                p,
                x,
                y - (15 + (i + 1) * 10),
                (str(i+1), record['name'], record['type'], record['barcode']),
            )

        p.drawString(x*6.5, inch, page_2)   # Page counter
        p.showPage()

    except Exception as e:
        error = str(e)
        print('[ERROR]: %s' % error)
        logger.debug(error)

    finally:
        p.save()

    return response


@csrf_exempt
@login_required
def upload_deep_sequencing_request(request):
    """ """
    error = ''
    file_name = ''
    file_path = ''

    if request.method == 'POST' and any(request.FILES):
        try:
            req = Request.objects.get(id=request.POST.get('request_id'))
            file = request.FILES.get('file')
            deep_seq_request = FileDeepSeqRequest(name=file.name, file=file)
            deep_seq_request.save()
            req.deep_seq_request = deep_seq_request
            req.save()
            file_name = deep_seq_request.name
            file_path = settings.MEDIA_URL + deep_seq_request.file.name

        except Exception as e:
            error = str(e)
            print('[ERROR]: %s' % error)
            logger.debug(error)

    return HttpResponse(
        json.dumps({
            'success': not error,
            'error': error,
            'name': file_name,
            'path': file_path,
        }),
        content_type='application/json',
    )
