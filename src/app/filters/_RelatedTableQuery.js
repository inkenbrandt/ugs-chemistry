define([
    'app/config',

    'dojo/_base/declare'
], function (
    config,

    declare
) {
    return declare(null, {
        // summary
        //      provides the ability to format a query to query against
        //      the results table

        // relatedTableQuery: Boolean (default: false)
        //      If true this is a query on the results table
        relatedTableQuery: false,

        getRelatedTableQuery: function (where) {
            // summary:
            //      Optionally wraps the where clause if it's applicable to the results table
            // where: String
            //      The original where clause
            console.log('app/filters/_RelatedTableQuery:getRelatedTableQuery', arguments);

            return (!this.relatedTableQuery) ?
                where : config.queryByResults + where + ')';
        }
    });
});