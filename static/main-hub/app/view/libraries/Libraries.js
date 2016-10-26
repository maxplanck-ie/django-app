Ext.define('MainHub.view.libraries.Libraries', {
    extend: 'Ext.container.Container',
    xtype: 'libraries',

    requires: [
        'MainHub.view.libraries.LibrariesController',
        'MainHub.view.libraries.LibraryWindow'
    ],

    controller: 'libraries-libraries',

    anchor : '100% -1',
    layout: 'fit',

    items: [
        {
            xtype: 'grid',
            id: 'librariesTable',
            itemId: 'librariesTable',
            height: Ext.Element.getViewportHeight() - 64,
            region: 'center',
            padding: 15,
            viewConfig: {
                stripeRows: false,
                getRowClass: function(record) {
                    return record.get('recordType') == 'L' ? 'library-row' : 'sample-row';
                }
            },

            header: {
                title: 'Libraries and Samples',
                items: [
                    {
                        xtype: 'fieldcontainer',
                        defaultType: 'checkboxfield',
                        layout: 'hbox',
                        margin: '0 20 0 0',
                        items: [
                            {
                                boxLabel: 'Show Libraries',
                                itemId: 'showLibrariesCheckbox',
                                margin: '0 15 0 0',
                                cls: 'grid-header-checkbox',
                                checked: true
                            },
                            {
                                boxLabel: 'Show Samples',
                                itemId: 'showSamplesCheckbox',
                                cls: 'grid-header-checkbox',
                                checked: true
                            }
                        ]
                    },
                    {
                        xtype: 'textfield',
                        itemId: 'searchField',
                        emptyText: 'Search',
                        width: 200
                    }
                ]
            },

            store: 'librariesStore',

            columns: {
                items: [
                    { text: 'Name', dataIndex: 'name', width: 150, renderer: function(val, meta) {
                        meta.tdStyle = 'font-weight:bold';
                        return val;
                    } },
                    { text: '', dataIndex: 'recordType', width: 30 },
                    { text: 'Barcode', dataIndex: 'barcode', width: 90 },
                    { text: 'Date', dataIndex: 'date' },
                    { text: 'Nucleic Acid Type', dataIndex: 'nucleicAcidTypeName' },
                    { text: 'Protocol', dataIndex: 'libraryProtocolName' },
                    { text: 'Library Type', dataIndex: 'libraryTypeName' },
                    { text: 'Enrichment Cycles', dataIndex: 'enrichmentCycles' },
                    { text: 'Amplified Cycles', dataIndex: 'amplifiedCycles' },
                    { text: 'Organism', dataIndex: 'organismName' },
                    { text: 'Index Type', dataIndex: 'indexTypeName' },
                    { text: 'Index Reads', dataIndex: 'indexReads' },
                    { text: 'Index I7', dataIndex: 'indexI7' },
                    { text: 'Index I5', dataIndex: 'indexI5' },
                    { text: 'Equal Representation', dataIndex: 'equalRepresentationOfNucleotides', renderer: function(val) {
                        return val ? 'Yes' : 'No';
                    } },
                    { text: 'DNA Dissolved In', dataIndex: 'DNADissolvedIn' },
                    { text: 'Concentration', dataIndex: 'concentration' },
                    { text: 'Concentration Determined By', dataIndex: 'concentrationDeterminedByName' },
                    { text: 'Sample Volume', dataIndex: 'sampleVolume' },
                    { text: 'Mean Fragment Size', dataIndex: 'meanFragmentSize' },
                    { text: 'qPCR Result', dataIndex: 'qPCRResult' },
                    { text: 'Sequencing Run Condition', dataIndex: 'sequencingRunConditionName' },
                    { text: 'Sequencing Depth', dataIndex: 'sequencingDepth' },
                    { text: 'DNase Treatment', dataIndex: 'DNaseTreatment', renderer: function(val) {
                        if (val == 'True') {
                            return 'Yes';
                        } else if (val == 'False') {
                            return 'No';
                        } else {
                            return '';
                        }
                    } },
                    { text: 'RNA Quality', dataIndex: 'rnaQualityName' },
                    { text: 'RNA Spike In', dataIndex: 'rnaSpikeIn', renderer: function(val) {
                        if (val == 'True') {
                            return 'Yes';
                        } else if (val == 'False') {
                            return 'No';
                        } else {
                            return '';
                        }
                    } },
                    { text: 'Sample Preparation Protocol', dataIndex: 'samplePreparationProtocol' },
                    { text: 'Requested Sample Treatment', dataIndex: 'requestedSampleTreatment' },
                    { text: 'Comments', dataIndex: 'comments' }
                ]
            },

            features: [{
                ftype:'grouping',
                groupHeaderTpl: '<strong>Request: {name}</strong> (No. of Libraries/Samples: {rows.length})'
            }],

            plugins: [{
                ptype: 'bufferedrenderer',
                trailingBufferZone: 100,
                leadingBufferZone: 100
            }]
        }
    ]
});
