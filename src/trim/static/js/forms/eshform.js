// console.log('multi-select.js')

// addEventListener('product-select', function(customEvent){
//     console.log('product-select', customEvent)
// })

/*

An Esh form is designed to offset some of the work when submiting djangoforms.

Wrap the _real_ node form in the view.

        liveForm = new EshForm('#productstash-form')

Add form items through addFormsetItems() or add()
Run the submit().

Notable this expects a JSON response from the backend.
 */
class EshForm {
    constructor(form, initData) {
        // node or string
        this._form = form
        this._formNode = undefined
        this._initData = initData
        console.log('New EshForm')
    }

    getFormNode(){
        if(this._formNode == undefined) {
            this._formNode = this.resolveForm()

            if(this._pushing == true) {
                console.error('Pushing init data whilst pushing init data.')
                throw Error('Cannot resolve a form when pushing into a new form.')
            }
            this._pushing = true
            this.pushInitData(this._formNode)
            console.log('Push complete')
            this._pushing = false
        }
        return this._formNode
    }

    pushInitData(formNode) {
        /* Given a form node, apply the init data as first content. */
        if(this._initData) {
            console.info('Pushing new data')
        }
        this.update(this._initData, formNode)
    }

    ensureInit() {
        return this.getFormNode()
    }
    resolveForm(){
        if(typeof(this._form) == 'string') {
            return document.querySelector(this._form)
        }
        return this._form
    }

    getFormData(formNode){
        if(this._formData == undefined) {
            formNode = formNode || this.getFormNode()
            let formData = new FormData(formNode)
            this._formData = formData

        }

        return this._formData
    }

    update(data, formNode) {
        let formData = this.getFormData(formNode)
        return this.add(data, undefined, undefined, formData, formNode)
    }

    add(key, value, fileName, formData, formNode){
        formData = formData || this.getFormData(formNode)

        if(typeof(key) == 'object' && value == undefined) {
            for(let k in key) {
                let v = key[k]
                formData.append(k, v)
                this.attemptFormApply(k, v, undefined, formNode)
            }
        } else {
            // normal string key
            formData.append(key, value)//, fileName?fileName:undefined)
            this.attemptFormApply(key,value, fileName, formNode)
        }
        return this
    }

    set(key, value, fileName, formData, formNode){
        formData = formData == undefined? this.getFormData(formNode): formData;
        formData.set(key, value)//, fileName?fileName:undefined)
        this.attemptFormApply(key,value, fileName, formNode)
        return this
    }

    attemptFormApply(key,value, fileName, formNode) {
        let node = this.getFormNodeField(key, formNode)
        if(node == null) {
            console.warn('Form field', key, 'cannot be applied.')
            return
        }
        let type = node.type
        let map = {
            text(value) {
                /* A texttype is easy to apply*/
                node.value = value
            }
            , textarea(value) {
                return this.text(value)
            }
        }

        if(map[type]) {
            return map[type](value)
        } else {
            console.warn(`attemptFormApply map for type "${type}" is not defined`)
        }
    }

    get(key) {
        return this.getFormData().get(key)
    }

    iterAdd(items, callable) {
        /* Given a list and a function, loop all items a call the function
        expecting a [key, value] pair.
        Insert into the existing formData
        */
        if(callable == undefined) {
            callable = (e,i,a, t) => [`key-${i}`, e]
        }
        let _this = this

        items.forEach(function(e, i, a){
            let [key, val] = callable(e,i,a, _this)
            if(key == undefined) {
                return
            }
            _this.add(key, val)
        })
    }

    items() {
        let formData = this.getFormData()
        let res = {}
        formData.forEach(function(e,i, a) {
            res[i] = e
        })
        return res
    }

    getMaxFormset() {
        let node = this.getFormNodeField('form-MAX_NUM_FORMS')
        return Number(node.value)
    }

    addFormsetItems(items) {

        // In this change, we remove the index, opting for a pure data count
        // as the store-down of this value polluates the next _pickup_
        let offsetIndex = 0 // this.getPushPostion()
        let callable = function(e, i, a, t) {
            let ci = offsetIndex + i
            if( typeof(e) == 'object' ) {
                for(let key in e) {
                    let str = `form-${ci}-${key}`
                    t.add(str, e[key])
                }
                return [undefined, undefined]
            }
            let str = `form-${ci}`
            return [str, e]
        }

        this.iterAdd(items, callable)
        this.setPushPosition(offsetIndex + items.length)
    }

    getPushPostion(){
        // return the current position of formset push items
        // usually this is TOTAL_FORMS
        let node = this.getFormNodeField('form-TOTAL_FORMS')
        return Number(node.value)
    }

    setPushPosition(value){
        // set the current position of formset
        // to the TOTAL_FORMS field
        let node = this.getFormNodeField('form-TOTAL_FORMS')
        node.value = value
        this.getFormData().set('form-TOTAL_FORMS', value)
    }

    getFormNodeField(name, formNode) {
        // return the real form node
        let node = formNode || this.getFormNode()
        return node.querySelector(`[name="${name}"]`)
    }

    getDataKeys(){
        return Array.from(this.getFormData().keys())
    }

    submit(callback) {
        let formData = this.getFormData()
        let node = this.getFormNode()

        let data = {
            body: formData,
            method: node.method,
        }

        let promise = fetch(node.action, data)
                        .then(this.handleSubmitResponse)
                        .catch((error) => {
                            console.error('Error:', error);
                        });
        if(callback) {
            promise.then(callback)
        }
        return promise
    }

    handleSubmitResponse(response){
        console.log('handleSubmitResponse', response)
        if (!response.ok) {
            throw new Error('Network response was not OK');
        }
        return response.json()
    }
}


const selectedProducts = new Set()
let liveForm = undefined;


const getLiveForm = function(){
    if(liveForm == undefined) {
        liveForm = getNodeForm()
    }
    return liveForm
}


const getNodeForm = function(selector){
    return (new EshForm(selector))
}


const getPopulatedLiveForm = function(){
    let lv = getLiveForm()
    let items = []
    for(let product_id of selectedProducts) {
        items.push({product_id})
    }
    lv.addFormsetItems(items)
    return lv
}


const getPopulatedForm = function(){
    let lv = getNodeForm()
    let items = []
    for(let product_id of selectedProducts) {
        items.push({product_id})
    }
    lv.addFormsetItems(items)
    return lv
}


const getProductId = function(pointerEvent) {
    let ck = pointerEvent.target
    return getProductIdFromNode(ck)
}


const getProductIdFromNode = function(node)  {
    let datakey = node.dataset.datakey || 'id'
    let id = node.dataset[datakey]
    if(id === undefined) { id = node.id }
    return id
}


const productSelectHook = function(pointerEvent){
    /* Stack a list of product ids into a Set, */
    let productId = getProductId(pointerEvent)
    // Push the value into the selected set.
    let func = ['delete', 'add'][Number(pointerEvent.target.checked)]
    selectedProducts[func](productId)
    console.log('hook product-select', selectedProducts)
}


const productSelectHookAll = function(pointerEvent, dataTarget){
    /*
    Check all items as _marked,
    get all _ids_ and insert into selected products.

        <input type="checkbox"
                name="product-select-all"
                onclick='announce("product-select-all", event, "product")'>

    js:
        hooks.add('product-select-all', productSelectHookAll)

     */
    let items = new Set()
    let checks = document.querySelectorAll(`input[data-group="${dataTarget}"]`)
    for(let node of checks) {
        let pid = getProductIdFromNode(node)
        items.add(pid)
    }

    let target = pointerEvent.target
    let checked = pointerEvent.target.checked
    let func = ['delete', 'add'][Number(checked)]

    // Select or _deselect_ items.
    for(let id of items) {
        selectedProducts[func](id)
        // and push back into the nodes.
        document.querySelector(`input[data-id="${id}"]`).checked = checked
    }

}


const productstashSend = function(pointerEvent) {
    /* Send all products to the push endpoint and announce the return.*/
    getPopulatedForm().submit().then(productstashSendResponse)
}


const productstashSendResponse = function(json) {
    /*
        <response-area for='productstash-response'></response-area>
     */
    let responseKey = 'productstash-response'
    let content = JSON.stringify(json, null, 4)

    hooks.call(responseKey, json)
    return toResponseArea(responseKey, content)
}

const toResponseArea = function(responseKey, inner){
    /* Print the content to a response area

        <response-area for='responseKey'></response-area>

    call with within the js to populate the html node:

        toResponseArea(responseKey, content)
    */
    let area = document.querySelector(`response-area[for="${responseKey}"]`)
    area.innerHTML = inner
    return area
}


if(window.hooks){
    hooks.add('product-select', productSelectHook)
    hooks.add('product-select-all', productSelectHookAll)
    hooks.add('productstash-send', productstashSend)
}
