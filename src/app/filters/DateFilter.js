define([
    'agrc/modules/Formatting',

    'app/config',
    'app/filters/_Filter',

    'dojo-bootstrap/Datepicker',

    'dojo/_base/declare',
    'dojo/_base/lang',
    'dojo/date',
    'dojo/date/locale',
    'dojo/dom-class',
    'dojo/on',
    'dojo/query',
    'dojo/string',
    'dojo/text!app/filters/templates/DateFilter.html',

    'xstyle/css!app/filters/resources/DateFilter.css'
], function (
    Formatting,

    config,
    _Filter,

    Datepicker,

    declare,
    lang,
    date,
    locale,
    domClass,
    on,
    query,
    dojoString,
    template
) {
    return declare([_Filter], {
        // description:
        //      Filter by from and to date.

        templateString: template,

        // Properties to be sent into constructor

        // fieldName: String
        fieldName: null,

        constructor: function () {
            // summary:
            //      apply base css class
            console.log('app/filters/DateFilter:constructor', arguments);

            this.baseClass += ' date-filter';
        },
        postCreate: function () {
            // summary:
            //      description
            console.log('app/filters/DateFilter:postCreate', arguments);

            this.from = new Datepicker(this.fromDate, {});
            on(this.fromDate, 'changeDate', lang.hitch(this, 'onChange'));
            this.to = new Datepicker(this.toDate, {});
            on(this.toDate, 'changeDate', lang.hitch(this, 'onChange'));

            this.inherited(arguments);
        },
        clear: function () {
            // summary:
            //      description
            console.log('app/filters/DateFilter:clear', arguments);

            this.fromDate.value = '';
            this.toDate.value = '';
            domClass.add(this.numSpan, 'hidden');

            this.emit('changed');
        },
        onChange: function () {
            // summary:
            //      on of the date pickers was changed
            console.log('app/filters/DateFilter:onChange', arguments);

            if (this.isValid()) {
                var num = Formatting.addCommas(date.difference(
                    this.from.date,
                    this.to.date
                ));
                this.numSpan.innerHTML = '(' + num + ' days)';
                domClass.remove(this.numSpan, 'hidden');
            } else {
                domClass.add(this.numSpan, 'hidden');
            }

            this.emit('changed');
        },
        isValid: function () {
            // summary:
            //      checks to make sure that there are valid dates
            console.log('app/filters/DateFilter:isValid', arguments);

            return this.fromDate.value.trim() && this.toDate.value.trim();
        },
        getQuery: function () {
            // summary:
            //      builds the where clause using the dates
            console.log('app/filters/DateFilter:getQuery', arguments);

            var formatDate = function (date) {
                return locale.format(date, {
                    selector: 'date',
                    datePattern: 'yyyy-MM-dd'
                });
            };
            if (this.isValid()) {
                var where = "${fieldName} >= date '${from}' AND ${fieldName} <= date '${to}')";
                return config.queryByResults + dojoString.substitute(where, {
                    fieldName: this.fieldName,
                    from: formatDate(this.from.date),
                    to: formatDate(this.to.date)
                });
            } else {
                return undefined;
            }
        }
    });
});
