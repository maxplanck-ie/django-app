Ext.define('MainHub.model.libraries.Library', {
    extend: 'MainHub.model.Base',

    fields: [
        {  name: 'requestName',                         type: 'string'  },
        {  name: 'requestId',                           type: 'int'     },
        {  name: 'libraryId',                           type: 'int'     },
        {  name: 'sampleId',                            type: 'int'     },
        {  name: 'name',                                type: 'string'  },
        {  name: 'recordType',                          type: 'string'  },
        {  name: 'date',                                type: 'string'  },
        {  name: 'libraryProtocol',                     type: 'int'     },
        {  name: 'libraryProtocolName',                 type: 'string'  },
        {  name: 'libraryType',                         type: 'string'  },
        {  name: 'libraryTypeId',                       type: 'int'     },
        {  name: 'enrichmentCycles',                    type: 'string'  },
        {  name: 'amplifiedCycles',                     type: 'string'  },
        {  name: 'organism',                            type: 'int'     },
        {  name: 'organismName',                        type: 'string'  },
        {  name: 'indexType',                           type: 'string'  },
        {  name: 'indexTypeId',                         type: 'int'     },
        {  name: 'indexReads',                          type: 'string'  },
        {  name: 'indexI7',                             type: 'string'  },
        {  name: 'indexI5',                             type: 'string'  },
        {  name: 'equalRepresentationOfNucleotides',    type: 'bool'    },
        {  name: 'DNADissolvedIn',                      type: 'string'  },
        {  name: 'concentration',                       type: 'string'  },
        {  name: 'concentrationDeterminedBy',           type: 'int'     },
        {  name: 'concentrationDeterminedByName',       type: 'string'  },
        {  name: 'sampleVolume',                        type: 'string'  },
        {  name: 'meanFragmentSize',                    type: 'string'  },
        {  name: 'qPCRResult',                          type: 'string'  },
        {  name: 'sequencingRunCondition',              type: 'int'     },
        {  name: 'sequencingRunConditionName',          type: 'string'  },
        {  name: 'sequencingDepth',                     type: 'string'  },
        {  name: 'comments',                            type: 'string'  },
        {  name: 'barcode',                             type: 'string'  },
        {  name: 'nucleicAcidType',                     type: 'int'     },
        {  name: 'nucleicAcidTypeName',                 type: 'string'  },
        {  name: 'DNaseTreatment',                      type: 'bool'    },
        {  name: 'rnaQuality',                          type: 'int'     },
        {  name: 'rnaQualityName',                      type: 'string'  },
        {  name: 'rnaSpikeIn',                          type: 'bool'    },
        {  name: 'samplePreparationProtocol',           type: 'string'  },
        {  name: 'requestedSampleTreatment',            type: 'string'  }
    ]
});
