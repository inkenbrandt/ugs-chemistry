define([
    'app/filters/_Filter',
    'app/filters/_RelatedTableQuery',

    'dojo/_base/declare',
    'dojo/text!app/filters/templates/FreeTypeFilter.html',

    'xstyle/css!app/filters/resources/FreeTypeFilter.css'
], function (
    _Filter,
    _RelatedTableQuery,

    declare,
    template
) {
    return declare([_Filter, _RelatedTableQuery], {
        // description:
        //      Auto complete text box

        templateString: template,


        // Properties to be sent into constructor

        // fieldName: String
        fieldName: null,

        constructor: function () {
            // summary:
            //      apply base class
            console.log('app/filters/FreeTypeFilter:constructor', arguments);

            this.baseClass += ' free-type-filter';
        },
        clear: function () {
            // summary:
            //      reset the controls
            console.log('app/filters/FreeTypeFilter:clear', arguments);

            this.txtBox.value = '';
            this.applyBtn.disabled = false;
            this.valueSpan.innerHTML = '';
            this.emit('changed');
        },
        onTxtBoxChange: function () {
            // summary:
            //      reset button
            console.log('app/filters/FreeTypeFilter:onTxtBoxChange', arguments);

            this.applyBtn.disabled = false;
        },
        onApplyClick: function () {
            // summary:
            //      set query
            console.log('app/filters/FreeTypeFilter:onApplyClick', arguments);

            this.valueSpan.innerHTML = this.txtBox.value;

            this.applyBtn.disabled = true;

            this.emit('changed');
        },
        getQuery: function () {
            // summary:
            //      returns the current query
            console.log('app/filters/FreeTypeFilter:getQuery', arguments);

            if (this.valueSpan.innerHTML !== '') {
                var where = this.fieldName + ' = \'' + this.valueSpan.innerHTML + '\'';
                return this.getRelatedTableQuery(where);
            } else {
                return undefined;
            }
        }
    });
});