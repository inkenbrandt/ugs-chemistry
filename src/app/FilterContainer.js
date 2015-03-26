define([
    'app/config',
    'app/filters/ListFilter',

    'dijit/_TemplatedMixin',
    'dijit/_WidgetBase',
    'dijit/_WidgetsInTemplateMixin',

    'dojo/_base/array',
    'dojo/_base/declare',
    'dojo/dom-construct',
    'dojo/text!app/templates/FilterContainer.html',

    'xstyle/css!app/resources/FilterContainer.css'
], function(
    config,
    ListFilter,

    _TemplatedMixin,
    _WidgetBase,
    _WidgetsInTemplateMixin,

    array,
    declare,
    domConstruct,
    template
) {
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        // description:
        //      Control for managing the filter for the application. Contains a vareity of FilterType's.

        templateString: template,
        baseClass: 'filter-container',
        widgetsInTemplate: true,

        // filters: _Filter[]
        //      list of filters for this widget
        filters: null,

        // Properties to be sent into constructor

        postCreate: function() {
            // summary:
            //      Overrides method of same name in dijit._Widget.
            // tags:
            //      private
            console.log('app/FilterContainer:postCreate', arguments);

            this.filters = [
                new ListFilter({
                    title: 'County',
                    items: config.counties,
                    parent: this.container
                }),
                new ListFilter({
                    title: 'State',
                    items: config.states,
                    parent: this.container
                })
            ];

            var that = this;
            var addOption = function (title, id) {
                domConstruct.create('option', {
                    innerHTML: title,
                    value: id
                }, that.select);
            };
            this.filters.forEach(function (f) {
                that.own(f);
                addOption(f.title, f.id);
                f.on('removed', function(filter) {
                    addOption(filter.title, filter.id);
                    that.container.removeChild(filter.domNode);
                });
            });

            this.inherited(arguments);
        },
        addFilter: function () {
            // summary:
            //      description
            console.log('app/FilterContainer:addFilter', arguments);
        
            var id = this.select.value;
            if (id !== 'none') {
                var filter = this.getFilter(id);
                domConstruct.place(filter.domNode, this.container);
                filter.open();
                array.some(this.select.children, function (option) {
                    if (option.value === id) {
                        domConstruct.destroy(option);
                        return true;
                    }
                });
            }
        },
        getFilter: function (id) {
            // summary:
            //      searches through the filters list and returns the one
            //      with the matching id
            // id: String
            console.log('app/FilterContainer:getFilter', arguments);
        
            var filter;
            this.filters.some(function (f) {
                filter = f;
                return f.id === id;
            });

            return filter;
        }
    });
});