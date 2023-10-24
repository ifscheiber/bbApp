

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        on_interaction_trend_column: function(cell_render_data, row_data, page_url) {
            // Check if 'clickData' is in cell_render_data['value']

            if (cell_render_data) {
                if ('clickData' in cell_render_data['value']) {
                    // Extract the date string
                    const dateString = cell_render_data['value']['clickData']['points'][0]['x'];

                    // remove focus from datepicker, as it will not be blurred
                    var datepicker = document.getElementById(`date_picker_home_id`)
                    datepicker.blur()

                    // Return  Date object
                    return new Date(dateString);
                }
            }
            // If 'clickData' is not present, return null (or another appropriate value)
            return window.dash_clientside.no_update;
        }
    }
});



