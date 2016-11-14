Ext.define('MainHub.model.pooling.LibraryPreparation', {
    extend: 'MainHub.model.Base',

    fields: [
        {  name: 'name',                    type: 'string'  },
        {  name: 'sampleId',                type: 'int'     },
        {  name: 'libraryProtocolName',     type: 'string'  },
        {  name: 'libraryProtocol',         type: 'int'     },
        {  name: 'concentrationSample',     type: 'string'  },
        {  name: 'startingAmount',          type: 'string'  },
        {  name: 'spikeInDescription',      type: 'string'  },
        {  name: 'spikeInVolume',           type: 'string'  },
        {  name: 'ulSample',                type: 'string'  },
        {  name: 'ulBuffer',                type: 'string'  },
        {  name: 'indexI7Id',               type: 'string'  },
        {  name: 'indexI5Id',               type: 'string'  },
        {  name: 'pcrCycles',               type: 'string'  },
        {  name: 'concentrationLibrary',    type: 'string'  },
        {  name: 'meanFragmentSize',        type: 'string'  },
        {  name: 'nM',                      type: 'string'  },
        {  name: 'libraryQC',               type: 'string'  }
    ]
});