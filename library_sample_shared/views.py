import json
import logging

from django.http import JsonResponse
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from common.utils import JSONResponseMixin
from common.views import StandardResultsSetPagination
from request.models import Request

from .models import (Organism, ReadLength, LibraryProtocol, LibraryType,
                     IndexType, IndexI7, IndexI5, ConcentrationMethod)

from .serializers import (OrganismSerializer, IndexTypeSerializer,
                          LibraryProtocolSerializer, LibraryTypeSerializer,
                          IndexI7Serializer, IndexI5Serializer,
                          ReadLengthSerializer, ConcentrationMethodSerializer)

logger = logging.getLogger('db')


class MoveOtherMixin(object):
    """ Move the 'Other' option to the end of the returning list. """

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self._get_data(serializer))

        serializer = self.get_serializer(queryset, many=True)
        return Response(self._get_data(serializer))

    def _get_data(self, serializer):
        data = serializer.data

        # Move the 'Other' option to the end of the list
        other_options = sorted([
            x for x in data if 'Other' in x['name']
        ], key=lambda x: x['name'])

        for other in other_options:
            index = data.index(other)
            data.append(data.pop(index))

        return data


class SimpleStoreView(JSONResponseMixin, ListView):
    """ Base class for simple Ext JS stores (with "id" and "name" only). """
    def render_to_response(self, context, **response_kwargs):
        response_kwargs['safe'] = False
        data = [
            {
                'id': obj.pk,
                'name': obj.name
            }
            for obj in context.pop('object_list')
        ]

        return self.render_to_json_response(data, **response_kwargs)


@login_required
def get_index_types(request):
    """ Get the list of index types. """
    data = [
        {
            'id': index_type.pk,
            'name': index_type.name,
            'indexReads': [index_type.is_index_i7,
                           index_type.is_index_i5].count(True),
            'isDual': index_type.is_index_i7 and index_type.is_index_i5,
            'indexLength': int(index_type.get_index_length_display()),
        }
        for index_type in IndexType.objects.all()
    ]

    return JsonResponse(data, safe=False)


class IndexStoreView(JSONResponseMixin, ListView):
    """ Base class for IndexI7/IndexI5 stores. """
    def render_to_response(self, context, **response_kwargs):
        response_kwargs['safe'] = False

        index_type = int(self.request.GET.get('index_type_id'))
        all_indices = context.pop('object_list')
        indices = all_indices.filter(index_type=index_type)

        data = [
            {
                'id': index.id,
                'name': '%s - %s' % (index.index_id, index.index),
                'index': index.index,
                'indexId': index.index_id,
            }
            for index in indices
        ]
        data = sorted(data, key=lambda x: x['id'])
        return self.render_to_json_response(data, **response_kwargs)


@login_required
def get_library_protocols(request):
    """ Get the list of all library protocols. """
    data = []

    if request.method == 'GET':
        na_type = request.GET.get('type', '')  # Nucleic Acid Type
        if na_type:
            library_protocols = LibraryProtocol.objects.filter(type=na_type)
        else:
            library_protocols = LibraryProtocol.objects.all()

        data = [
            {
                'id': protocol.id,
                'name': protocol.name,
                'type': protocol.type,
                'provider': protocol.provider,
                'catalog': protocol.catalog,
                'explanation': protocol.explanation,
                'inputRequirements': protocol.input_requirements,
                'typicalApplication': protocol.typical_application,
                'comments': protocol.comments,
            }
            for protocol in library_protocols
        ]
        data = sorted(data, key=lambda x: x['name'])

        # Move the 'Other' option to the end of the list
        # other = [x for x in data if 'Other' in x['name']]
        other_options = sorted([
            x for x in data
            if x['name'] == 'Other - DNA Methods' or
            x['name'] == 'Other - RNA Methods'
        ], key=lambda x: x['name'])

        for other in other_options:
            index = data.index(other)
            data.append(data.pop(index))

    return JsonResponse(data, safe=False)


@login_required
def get_library_types(request):
    """ Get the list of all library types. """
    data = []

    if request.method == 'GET':
        library_protocol_id = request.GET.get('library_protocol_id', '')

        if library_protocol_id:
            lib_protocol = LibraryProtocol.objects.get(pk=library_protocol_id)
            library_types = LibraryType.objects.filter(
                library_protocol__in=[lib_protocol]
            )

            protocol = {}
            for lib_type in library_types:
                protocol[lib_type.pk] = [lib_protocol.pk]

        else:
            library_types = LibraryType.objects.all()
            protocol = {}

            # Collect all library protocols for each library type
            for lib_type in library_types:
                protocol[lib_type.pk] = [
                    library_protocol.pk
                    for library_protocol in lib_type.library_protocol.all()
                ]

        data = [
            {
                'id': library_type.pk,
                'name': library_type.name,
                'protocol': protocol[library_type.pk]
            }
            for library_type in library_types
        ]

        # move 'Other' option to the end of the list
        other = [x for x in data if x['name'] == 'Other']
        if other:
            index = data.index(other[0])
            data.append(data.pop(index))

    return JsonResponse(data, safe=False)


class OrganismViewSet(MoveOtherMixin, viewsets.ReadOnlyModelViewSet):
    """ Get the list of organisms. """
    queryset = Organism.objects.order_by('name')
    serializer_class = OrganismSerializer


class ReadLengthViewSet(viewsets.ReadOnlyModelViewSet):
    """ Get the list of read lengths. """
    queryset = ReadLength.objects.all()
    serializer_class = ReadLengthSerializer


class ConcentrationMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """ Get the list of concentration methods. """
    queryset = ConcentrationMethod.objects.order_by('name')
    serializer_class = ConcentrationMethodSerializer


class IndexTypeViewSet(MoveOtherMixin, viewsets.ReadOnlyModelViewSet):
    """ Get the list of index types. """
    queryset = IndexType.objects.order_by('name')
    serializer_class = IndexTypeSerializer


class IndexViewSet(viewsets.ViewSet):

    def list(self, request):
        """ Get the list of all indices. """
        index_i7_serializer = IndexI7Serializer(
            IndexI7.objects.all(), many=True)
        index_i5_serializer = IndexI5Serializer(
            IndexI5.objects.all(), many=True)
        indices = index_i7_serializer.data + index_i5_serializer.data
        data = sorted(indices, key=lambda x: x['index_id'])
        return Response(data)

    @list_route(methods=['get'])
    def i7(self, request):
        """ Get the list of indices i7. """
        queryset = self._get_index_queryset(IndexI7)
        serializer = IndexI7Serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def i5(self, request):
        """ Get the list of indices i5. """
        queryset = self._get_index_queryset(IndexI5)
        serializer = IndexI5Serializer(queryset, many=True)
        return Response(serializer.data)

    def _get_index_queryset(self, model):
        queryset = model.objects.order_by('index_id')
        index_type = self.request.query_params.get('index_type_id', None)
        if index_type is not None:
            try:
                queryset = queryset.filter(index_type=index_type)
            except ValueError:
                queryset = []
        return queryset


class LibraryProtocolViewSet(MoveOtherMixin, viewsets.ReadOnlyModelViewSet):
    """ Get the list of library protocols. """
    serializer_class = LibraryProtocolSerializer

    def get_queryset(self):
        queryset = LibraryProtocol.objects.order_by('name')
        na_type = self.request.query_params.get('type', None)
        if na_type is not None:
            queryset = queryset.filter(type=na_type)
        return queryset


class LibraryTypeViewSet(MoveOtherMixin, viewsets.ReadOnlyModelViewSet):
    """ Get the list of library types. """
    serializer_class = LibraryTypeSerializer

    def get_queryset(self):
        queryset = LibraryType.objects.order_by('name')
        library_protocol = self.request.query_params.get(
            'library_protocol_id', None)
        if library_protocol is not None:
            try:
                queryset = queryset.filter(
                    library_protocol__in=[library_protocol])
            except ValueError:
                queryset = []
        return queryset


class LibrarySampleBaseViewSet(viewsets.ViewSet):
    pagination_class = StandardResultsSetPagination

    # TODO: either add pagination or remove at all
    def list(self, request):
        """ Get the list of all libraries or samples. """
        data = []
        requests_queryset = Request.objects.order_by('-create_time')
        if not request.user.is_staff:
            requests_queryset = requests_queryset.filter(user=request.user)
        for request_obj in requests_queryset:
            # TODO: sort by item['barcode'][3:]
            records = getattr(request_obj, self.model_name_plural.lower())
            serializer = self.serializer_class(
                records.order_by('barcode'), many=True)
            data += serializer.data
        return Response(data)

    def create(self, request):
        """ Add new libraries/samples. """
        post_data = json.loads(request.POST.get('data', '[]'))

        if not post_data:
            return Response({
                'success': False,
                'message': 'Invalid payload.',
            }, 400)

        serializer = self.serializer_class(data=post_data, many=True)
        if serializer.is_valid():
            objects = serializer.save()
            data = [{
                'pk': obj.pk,
                'record_type': self.model_name,
                'name': obj.name,
                'barcode': obj.barcode,
            } for obj in objects]
            return Response({'success': True, 'data': data}, 201)

        else:
            # Try to create valid records
            valid_data = [item[1] for item in zip(serializer.errors, post_data)
                          if not item[0]]

            if any(valid_data):
                message = 'Invalid payload. Some records cannot be added.'
                objects = self._create_or_update_valid(valid_data)

                data = [{
                    'pk': obj.pk,
                    'record_type': self.model_name,
                    'name': obj.name,
                    'barcode': obj.barcode,
                } for obj in objects]

                return Response({
                    'success': True,
                    'message': message,
                    'data': data,
                }, 201)

            else:
                # logger.debug('POST DATA', post_data)
                # logger.debug('VALIDATION ERRORS', serializer.errors)
                return Response({
                    'success': False,
                    'message': 'Invalid payload.',
                }, 400)

    def retrieve(self, request, pk=None):
        """ Get a library/sample with a given id. """
        try:
            obj = self.model_class.objects.get(pk=int(pk))
            serializer = self.serializer_class(obj)
            return Response({
                'success': True,
                'data': serializer.data
            })

        except ValueError:
            return Response({
                'success': False,
                'message': 'Id is not provided.',
            }, 400)

        except self.model_class.DoesNotExist:
            return Response({
                'success': False,
                'message': '%s does not exist.' % self.model_name,
            }, 404)

    @list_route(methods=['post'])
    def edit(self, request):
        """ Update multiple libraries/samples. """
        post_data = json.loads(request.POST.get('data', '[]'))

        if not post_data:
            return Response({
                'success': False,
                'message': 'Invalid payload.',
            }, 400)

        ids = [x['pk'] for x in post_data]
        objects = self.model_class.objects.filter(pk__in=ids)
        serializer = self.serializer_class(data=post_data, instance=objects,
                                           many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})

        else:
            # Try to update valid records
            valid_data = [item[1] for item in zip(serializer.errors, post_data)
                          if not item[0]]

            if any(valid_data):
                message = 'Invalid payload. Some records cannot be updated.'
                ids = [x['pk'] for x in valid_data]
                self._create_or_update_valid(valid_data, ids)
                return Response({'success': True, 'message': message}, 200)

            else:
                return Response({
                    'success': False,
                    'message': 'Invalid payload.',
                }, 400)

    # @list_route(methods=['post'])
    # def delete(self, request):
    #     pass

    def destroy(self, request, pk=None):
        """ Delete a library/sample with a given id. """
        try:
            obj = self.model_class.objects.get(pk=int(pk))
            obj.delete()
            return Response({'success': True})

        except ValueError:
            return Response({
                'success': False,
                'message': 'Id is not provided.',
            }, 400)

        except self.model_class.DoesNotExist:
            return Response({
                'success': False,
                'message': '%s does not exist.' % self.model_name,
            }, 404)

    def _create_or_update_valid(self, valid_data, ids=None):
        """ Create or update valid objects. """
        if not ids:
            serializer = self.serializer_class(data=valid_data, many=True)
        else:
            objects = self.model_class.objects.filter(pk__in=ids)
            serializer = self.serializer_class(
                data=valid_data, instance=objects, many=True)
        serializer.is_valid()
        return serializer.save()
