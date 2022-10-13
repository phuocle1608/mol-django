function isNumeric(value) {
    return /^\d+$/.test(value);
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function generateSelectHTML(xdict) {
    const html_arr = []
    for (let x in xdict) {
        html_arr.push(`<option value="${x}">${xdict[x]}</option>`)
    }
//    html_arr.push('</select>')
    return `<select name="myEditSelect"> ${html_arr.join(' ')} </select>`
//    return html_arr.join(' ')
}


$(document).ready(function () {
     /**
     * Set up th edit in place items
     */
     //Simple inline edit
     // $('.dedit-simple').doomEdit({
     //    ajaxSubmit: false,
     //    placeholder: true,
     //    afterFormSubmit: function (data, form, el) {
     //       el.text(data);
     //       console.log(el.0.attributes.id.value);
     //       $.ajax({
     //          type: 'POST',
     //          url: "{% url 'test' %}",
     //          data: {
     //             'csrfmiddlewaretoken': "{{  csrf_token  }}",
     //             "value": data,
     //             "id": el.0.attributes.id.value

     //          },
     //          success: function (response) {
     //             // if not valid user, alert the user
     //             console.log(1)
     //          },
     //          error: function (response) {
     //             console.log(2)
     //          }
     //       })
     //    }
     // });
     //Simple inline edit with save on outside click
     $('.dedit-simple-blur').doomEdit({
        ajaxSubmit: false,
        submitOnBlur: true,
        submitBtn: false,
        cancelBtn: false,
        afterFormSubmit: function (data, form, el) {

            var current = el
            if (isNumeric(data)) {
                el.text(numberWithCommas(data));
                $.ajax({
                   type: 'POST',
                   url: xpath_url,
                   data: {
                       "csrfmiddlewaretoken" : csrf_token,
                       "value": data,
                       "donhang_id": el[0].attributes["donhang_id"].value,
                       "post-type": el[0].attributes["post-type"].value

                   },
                   success: function (response) {
                       // if not valid user, alert the user
                       console.log(1)
                   },
                   error: function (response) {
                       console.log(2)
                   }
                });

                let new_deft = el.parent().parent()[0].children[8].innerText.replaceAll(",", "") - data
                if (new_deft < 0) {
                    new_deft = 0
                }
                el.parent().parent()[0].children[10].innerText = numberWithCommas(new_deft)
            }

        }
     });
     //Inline edit with textarea
     $('.dedit-textarea').doomEdit({ ajaxSubmit: false, editField: '<textarea name="myEditTextarea" rows="10" cols="70"></textarea>', afterFormSubmit: function (data, form, el) { el.text(data); } });
     //Inline edit with select
     $('.dedit-select').doomEdit({
        ajaxSubmit: false,
        submitOnBlur: true,
        submitBtn: false,
        cancelBtn: false,
        editField: generateSelectHTML(workingstatus_data),
        afterFormSubmit: function (data, form, el) {
            console.log(data)
            console.log(workingstatus_data)
            console.log(Object.keys(workingstatus_data))
            if (Object.keys(workingstatus_data).includes(data)) {
                el.text(workingstatus_data[data]);
                $.ajax({
                   type: 'POST',
                   url: xpath_url,
                   data: {
                       "csrfmiddlewaretoken" : csrf_token,
                       "value": data,
                       "donhang_id": el[0].attributes["donhang_id"].value,
                       "post-type": el[0].attributes["post-type"].value,
                   },
                   success: function (response) {
                       // if not valid user, alert the user
                       console.log(1)
                   },
                   error: function (response) {
                       console.log(2)
                   }
                });
            }

        }
     });
     //Inline edit and remote save with ajax
     $('.dedit-remote').doomEdit({ editForm: { method: 'post', action: 'remote.html', id: 'myeditformid' }, afterFormSubmit: function (data, form, el) { el.text($('input', form).val()); alert(data); } });
     //Inline edit and remote save with ajax with JSON response
     $('.dedit-remote-json').doomEdit({ editForm: { method: 'post', action: 'remote_json.html', id: 'myeditformid' }, afterFormSubmit: function (data, form, el) { data = $.parseJSON(data); el.text(data.message); alert(data.message); } });
     //Edit multiple cells inline
     $('.edit-cell-inline').doomEdit({ ajaxSubmit: false, afterFormSubmit: function (data, form, el) { el.text(data); } });
  });