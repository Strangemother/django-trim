
class QuickFetch {
    /* Use the fetch() and callback API without the overhead.
        Perform a 'quick fetch' for the tiny callbacks:

        + Real forms with FormData
        + fetch() api
        + promise or callback friendly.

        Create an instance, with some optional _default_ data for every call.

            const quickFetch = new QuickFetch({
                csrfmiddlewaretoken: PRODUCT_ATTRIBUTETITLE_CSRF_TOKEN,
            })

        Then get, post, fetch an endpoint:

            quickFetch.post('/products/attributetitle/search/', {
                query: 'apples'
            }).then(handleEnsure)

            const handleEnsure(data) {
                console.log('result', data)
            }

        ---

            this.quickFetch = new QuickFetch({
                csrfmiddlewaretoken: PRODUCT_ATTRIBUTETITLE_CSRF_TOKEN,
            })

            let data = {
                query: ''
            }

            let url = '/products/attributetitle/search/'
            this.quickFetch
                .post(url, data)
                .then(this.handleEnsure)
                ;

        Or with a callHook:

            var productAttributesCallbackConf = {
                url: "{% url 'products:attributetitle-json-form' %}"
                , method: 'POST'// is overridden at calltime.
                , defaults: {
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                }
            }

            // QuickFetch.productAttributes = QuickFetch.callHook(productAttributesCallbackConf)
            QuickFetch.callHook('productAttributes', productAttributesCallbackConf)

        Call Methods:
            // QuickFetch.productAttributes(data).then(this.handleEnsure)
            productAttributesQF.post(data).then(this.handleEnsure)
            productAttributesQF.post(url, data).then(this.handleEnsure)
            productAttributesQF.post(url, data, this.handleEnsure)
    */

    constructor(defaults={}, conf={}) {
        this.defaults = defaults
        this.conf = conf
    }

    static setup(conf){
        /*

            var productAttributesCallbackConf = {
                url: "{% url 'products:attributetitle-json-form' %}"
                , method: 'POST'// is overridden at calltime.
                , defaults: {
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                }
            }
            const productAttributesQF = QuickFetch.setup(productAttributesCallbackConf)


        QuickFetch.setup({
            url: "{% link 'products:attributetitle-json-form' %}"
            , defaults: {
                csrfmiddlewaretoken: '{{ csrf_token }}'
            }
            url: "{% link 'products:attributetitle-json-form' '__placeholder__' %}"
            placeholders: {
                __placeholder__(formData){
                    // A function called to replace the function name with
                    // the value
                    return formData.get('value')
                }
                // Or just a string for the form key
                , __placeholder__: 'value'
            }
        })
        */
        return (new this(conf.defaults, conf) )
    }

    static callHook(name_or_conf, alt_conf) {
        /*

            var productAttributesCallbackConf = {
                url: "{% url 'products:attributetitle-json-form' %}"
                , method: 'POST'// is overridden at calltime.
                , defaults: {
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                }
            }

            // QuickFetch.productAttributes = QuickFetch.callHook(productAttributesCallbackConf)
            QuickFetch.callHook('productAttributes', productAttributesCallbackConf)

        then use with:

            QuickFetch.productAttributes(data).then(this.handleEnsure)
         */
        let givenConf = name_or_conf
        let name = undefined
        if(alt_conf != undefined) {
            givenConf = alt_conf
            name = name_or_conf
        }

        let hookScope = function(parentClass, conf) {

            let scope = this;
            console.log('create hookScope')

            let hook = function(data, callback) {
                console.log('call hook hookScope', conf)
                let r = parentClass.setup(conf)
                return r.fetch(undefined, data, undefined, callback)
            }.bind({scope})

            return hook

        }.bind({parent: this, givenConf})

        let v = new hookScope(this, givenConf)
        v.post = function(){
            console.log('call foo on', this)
        }

        if(name != undefined) {
            console.log('Assigning to', this, name)
            this[name] = v;
        }

        return v
    }

    post(url, data, callback) {
        if(typeof(url) != 'string') {
            [url, data, callback] = [this.conf.url, data, callback]
        }

        return this.fetch(url, data, 'POST', callback)
    }

    get(url, data, callback) {
        return this.fetch(url, data, 'GET', callback)
    }

    put(url, data, callback) {
        return this.fetch(url, data, 'GET', callback)
    }

    fetch(url, body, method, callback) {
        let td = Object.assign({}, this.defaults, body)
        let formData = new FormData()

        method = method? method: this.conf.method
        url = url? url: this.conf.url

        for(let key in td) {
            let value = td[key];
            formData.set(key, value)//, fileName?fileName:undefined)
        }

        let data = {
            body: formData,
            method: method,
        }

        let promise = fetch(url, data)
                        .then(this.handleSubmitResponse)
                        .catch(this.error)
                        ;

        if(callback) {
            promise.then(callback)
        }
        return promise
    }

    error(error){
        console.error('Error:', error);
    }

    handleSubmitResponse(response){
        console.log('handleSubmitResponse', response)
        if (!response.ok) {
            throw new Error('Network response was not OK');
        }
        return response.json()
    }

    addDefaults(data) {
        this.defaults.assign(data)
    }
}


EshForm.quick = new QuickFetch
