require([
    'app/FilterContainer',

    'dojo/_base/array'
], function (
    FilterContainer,

    array
) {
    describe('app/FilterContainer', function () {
        var testWidget;
        beforeEach(function () {
            testWidget = new FilterContainer();
        });
        afterEach(function() {
            if (testWidget) {
                if (testWidget.destroy) {
                    testWidget.destroy();
                }

                testWidget = null;
            }
        });
        it('sanity', function () {
            expect(testWidget).toEqual(jasmine.any(FilterContainer));
        });
        describe('postCreate', function () {
            it('creates the filters', function () {
                expect(testWidget.filters.length > 0).toBe(true);
            });
        });
        describe('addFilter', function () {
            it('adds the filter to the container', function () {
                testWidget.select.value = testWidget.filters[0].id;
                testWidget.addFilter();

                expect(testWidget.container.children[0]).toBe(testWidget.filters[0].domNode);
            });
            it('shouldn\'t do anything if none is selected', function () {
                spyOn(testWidget, 'getFilter');
                testWidget.select.value = 'none';
                testWidget.addFilter();

                expect(testWidget.getFilter).not.toHaveBeenCalled();
            });
            it('removes the filter from the select', function () {
                testWidget.select.value = testWidget.filters[0].id;
                testWidget.addFilter();

                expect(array.every(testWidget.select.children, function (option) {
                    return option.value !== testWidget.filters[0].id;
                })).toBe(true);
            });
        });
    });
});