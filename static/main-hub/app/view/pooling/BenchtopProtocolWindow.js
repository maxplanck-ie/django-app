Ext.define('MainHub.view.pooling.BenchtopProtocolWindow', {
    extend: 'Ext.window.Window',
    // xtype: 'library-preparation',

    requires: ['MainHub.view.pooling.BenchtopProtocolWindowController'],

    controller: 'benchtop-protocol-window',

    title: 'Download Benchtop Protocol',
    height: 400,
    width: 280,

    modal: true,
    resizable: false,
    layout: 'fit',
    bodyPadding: 15,
    border: 0,

    items: [{
        border: 0,
        layout: 'vbox',
        items: [
            {
                html: '<strong>Choose parameters:</strong>',
                margin: '0 0 15px',
                border: 0
            },
            {
                xtype: 'form',
                id: 'benchtopProtocolParams',
                layout: 'fit',
                border: 0,
                standardSubmit: true,

                items: [{
                    xtype: 'fieldcontainer',
                    defaultType: 'checkbox',
                    items: [
                        {
                            boxLabel: 'Concentration Sample (ng/µl)',
                            inputValue: 'Concentration Sample (ng/µl)',
                            name: 'params',
                            id: 'concentrationSampleCb'
                        },
                        {
                            boxLabel: 'Starting Amount (ng)',
                            inputValue: 'Starting Amount (ng)',
                            name: 'params',
                            id: 'startingAmountCb'
                        },
                        {
                            boxLabel: 'Starting Volume (ng)',
                            inputValue: 'Starting Volume (ng)',
                            name: 'params',
                            id: 'startingVolumeCb'
                        },
                        {
                            boxLabel: 'Spike-in Volume (µl)',
                            inputValue: 'Spike-in Volume (µl)',
                            name: 'params',
                            id: 'spikeInVolumeCb'
                        },
                        {
                            boxLabel: 'µl Sample',
                            inputValue: 'µl Sample',
                            name: 'params',
                            id: 'ulSampleCb'
                        },
                        {
                            boxLabel: 'µl Buffer',
                            inputValue: 'µl Buffer',
                            name: 'params',
                            id: 'ulBufferCb'
                        }
                    ]
                }]
            }
        ]
    }],

    bbar: [
        {
            text: 'Select All',
            itemId: 'selectAll'
        },
        '->',
        {
            text: 'Download',
            itemId: 'download'
        }
    ],
});
