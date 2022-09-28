
const jsonDispatch = function(event){
    /*
        <div class="note-form">
            <form action="" id=master_note_form method="post">
                {% csrf_token %}
                <ul>
                    {{ form.as_ul }}
                </ul>
                <button type="submit" onclick="jsonDispatch(event)">Save</button>
            </form>
        </div>
     */
    event.stopImmediatePropagation()
    // event.stopPropagation()
    event.preventDefault()
    let res = ajaxPost(event.currentTarget.parentElement)
    return false
}

const ajaxPost = function(form, path=document.location.pathname) {
    /*
        Using ES6 fetch() api, perform a POST for the given "form" to the target
        "path". If no path is given, the current relative document location is
        used.

        This will post _a form_, as if someone pressed "submit". The standard
        django view accepts the form as a normal post.

        Steps should be taken to ensure the response flow matches the request
        method - in future versions the HTML header "is_ajax" does not exist -
        a _json_ flagged should be sent if a switch is required.
     */
    if(form == undefined) {
        let forms = document.querySelectorAll('form');
        if(forms.length > 1) {
            throw Error('More than one form found', form)
        }
        form = forms[0]
    }

    return fetch(path, {method: 'post', body: new FormData(form) })
}

