require([
    'app/config',
    'app/filters/ListFilter'
], function (
    config,
    ListFilter
) {

    describe('app/filters/ListFilter', function () {
        var testWidget;
        beforeEach(function () {
            testWidget = new ListFilter({
                items: [
                    ['desc1', 'value1'],
                    ['desc2', 'value2'],
                    ['desc3', 'value3']
                ],
                fieldName: 'FieldName',
                fieldType: ListFilter.TYPE_TEXT,
                anyAllToggle: true
            });
        });
        afterEach(function () {
            if (testWidget) {
                if (testWidget.destroy) {
                    testWidget.destroy();
                }

                testWidget = null;
            }
        });
        it('should create a ListFilter', function () {
            expect(testWidget).toEqual(jasmine.any(ListFilter));
        });
        describe('postCreate', function () {
            it('creates bubbles', function () {
                expect(testWidget.buttonContainer.children.length).toBe(3);
                expect(testWidget.buttonContainer.children[1].value).toBe('value2');
            });
        });
        describe('itemClicked', function () {
            it('add to the selected items array', function () {
                testWidget.itemClicked('1');
                expect(testWidget.selectedValues).toEqual(['1']);

                testWidget.itemClicked('2');
                expect(testWidget.selectedValues).toEqual(['1', '2']);
            });
            it('removes if it\'s already been selected', function () {
                testWidget.itemClicked('1');
                testWidget.itemClicked('2');

                testWidget.itemClicked('1');
                expect(testWidget.selectedValues).toEqual(['2']);
            });
        });
        describe('getQuery', function () {
            it('returns undefined if no items are selected', function () {
                expect(testWidget.getQuery()).not.toBeDefined();
            });
            it('returns a def query if some are selected', function () {
                testWidget.itemClicked('1');
                testWidget.itemClicked('2');

                expect(testWidget.getQuery()).toBe("FieldName IN ('1', '2')");

                testWidget.fieldType = ListFilter.TYPE_NUMBER;

                expect(testWidget.getQuery()).toBe("FieldName IN (1, 2)");
            });
            it('handles "all" queries', function () {
                testWidget.any = false;
                testWidget.itemClicked('1');
                testWidget.itemClicked('2');
                var expected = "FieldName = '1' AND FieldName = '2'";

                expect(testWidget.getQuery()).toBe(expected);

                testWidget.relatedTableQuery = true;

                expected = config.queryByResults + "FieldName = '1') AND " +
                     config.queryByResults + "FieldName = '2')";

                expect(testWidget.getQuery()).toBe(expected);
            });
            it('prepend related table queries', function () {
                testWidget.relatedTableQuery = true;

                testWidget.itemClicked('1');
                testWidget.itemClicked('2');

                expect(testWidget.getQuery()).toBe(config.queryByResults + "FieldName IN ('1', '2'))");
            });
        });
    });
});
