Ext.define('MainHub.model.qualitycontrol.IncomingLibraries', {
    extend: 'MainHub.model.libraries.Library',

    fields: [{
            name: 'dilutionFactor',
            type: 'string'
        },
        {
            name: 'concentrationFacility',
            type: 'string'
        },
        {
            name: 'concentrationMethodFacility',
            type: 'string'
        },
        {
            name: 'concentrationMethodFacilityId',
            type: 'int'
        },
        {
            name: 'dateFacility',
            type: 'string'
        },
        {
            name: 'sampleVolumeFacility',
            type: 'string'
        },
        {
            name: 'amountFacility',
            type: 'string'
        },
        {
            name: 'sizeDistributionFacility',
            type: 'string'
        },
        {
            name: 'commentsFacility',
            type: 'string'
        },
        {
            name: 'qPCRResultFacility',
            type: 'string'
        },
        {
            name: 'rnaQualityFacility',
            type: 'string'
        }
    ],

    getRecordType: function() {
        return (this.get('sampleId') === 0) ? 'L' : 'S';
    }
});
