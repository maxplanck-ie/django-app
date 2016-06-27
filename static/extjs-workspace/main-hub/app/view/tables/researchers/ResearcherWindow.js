Ext.define('MainHub.view.tables.researchers.ResearcherWindow', {
    extend: 'Ext.window.Window',
    alias: 'researcher_wnd',
    xtype: 'researcher_wnd',

    requires: [
        'MainHub.view.tables.researchers.ResearcherWindowController',
        'MainHub.view.tables.researchers.ResearcherFieldWindow'
    ],

    controller: 'researcher_wnd',

    height: 470,
    width: 400,

    modal: true,
    resizable: false,

    items: [
        {
            xtype: 'form',
            id: 'researcherForm',
            itemId: 'researcherForm',
            layout: 'anchor',
            border: 0,
            padding: 15,

            defaultType: 'textfield',
            defaults: {
                submitEmptyText: false,
                allowBlank: false,
                anchor: '100%'
            },

            items: [
                {
                    name: 'firstName',
                    fieldLabel: 'First name',
                    emptyText: 'First name'
                },
                {
                    name: 'lastName',
                    fieldLabel: 'Last name',
                    emptyText: 'Last name'
                },
                {
                    name: 'telephone',
                    fieldLabel: 'Telephone',
                    emptyText: 'Telephone'
                },
                {
                    name: 'email',
                    fieldLabel: 'Email',
                    emptyText: 'Email'
                },
                {
                    xtype: 'container',
                    layout: 'hbox',
                    items: [
                        {
                            xtype: 'combobox',
                            name: 'organization',
                            id: 'organizationField',
                            itemId: 'organizationField',
                            queryMode: 'local',
                            displayField: 'name',
                            valueField: 'organizationId',
                            fieldLabel: 'Organization',
                            emptyText: 'Organization',
                            store: 'organizationsStore',
                            forceSelection: true,
                            width: 331
                        },
                        {
                            xtype: 'button',
                            id: 'addOrganizationBtn',
                            iconCls: 'x-fa fa-plus'
                        }
                    ]
                },
                {
                    xtype: 'container',
                    layout: 'hbox',
                    items: [
                        {
                            xtype: 'combobox',
                            name: 'pi',
                            id: 'piField',
                            queryMode: 'local',
                            displayField: 'name',
                            valueField: 'piId',
                            fieldLabel: 'Principal Investigator',
                            emptyText: 'Principal Investigator',
                            store: 'principalInvestigatorsStore',
                            forceSelection: true,
                            disabled: true,
                            width: 331
                        },
                        {
                            xtype: 'button',
                            id: 'addPiBtn',
                            iconCls: 'x-fa fa-plus',
                            margin: '5px 0 0 0',
                            disabled: true
                        }
                    ]
                },
                {
                    xtype: 'container',
                    layout: 'hbox',
                    items: [
                        {
                            xtype: 'tagfield',
                            name: 'costUnit',
                            id: 'costUnitField',
                            queryMode: 'local',
                            displayField: 'name',
                            valueField: 'costUnitId',
                            fieldLabel: 'Cost Unit',
                            store: 'costUnitsStore',
                            disabled: true,
                            width: 331
                        },
                        {
                            xtype: 'button',
                            id: 'addCostUnitBtn',
                            iconCls: 'x-fa fa-plus',
                            disabled: true
                        }
                    ]
                }
            ]
        }
    ],

    bbar: [
        '->',
        {
            xtype: 'button',
            itemId: 'cancelBtn',
            text: 'Cancel'
        },
        {
            xtype: 'button',
            itemId: 'addResearcherWndBtn',
            id: 'addResearcherWndBtn',
            text: 'Add',
            hidden: true
        },
        {
            xtype: 'button',
            itemId: 'editResearcherWndBtn',
            id: 'editResearcherWndBtn',
            text: 'Update',
            hidden: true
        }
    ]
});