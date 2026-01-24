urlpatterns = trim.paths_dict(
    views,
    dict(
        VacgenListView=("list", ""),
        VacgenNoImageListView=("noimage-list", "noimage/"),
        ProductBrandListView=("brands-list", "brands/"),
        ProductBrandDetailView=("brand", "brands/<str:origin_brand>/"),
        # ProductAttributeListView=('productattribute-list', 'filter/'),
        # AttributeTitleListView=('productattribute-list', 'filter/'),
        AttributeTitleListView=("productattribute-list", "filter/"),
        AttributeTitleDetailView=("attributetitle-detail", "filter/title/<str:pk>/"),
        ProductCategoryListView=("category-list", "category/"),
        ProductCategoryDetailView=("category", "category/<str:category_name>/"),
        ## Filter the list of products within an attributevalue list,
        ## using the inherited title; e.g. spares/yes  | power/yes
        AttributeTitleValueListView=(
            "attributetitle-value-list",
            "filter/<str:title_slug>/<str:pk>/",
        ),
        ProductStashListView=("productstash-list", "stash/"),
        ProductStashLabelFormView=(
            "productstash-label-form",
            "stash/form/<str:uuid>/label/",
        ),
        ProductStashMergeFormView=(
            "productstash-merge-form",
            "stash/form/<str:uuid>/merge/",
        ),
        ProductStashFormView=(
            "productstash-form",
            ("stash/form/", "stash/form/<str:uuid>/"),
        ),
        ProductStashDetailView=("productstash-detail", "stash/<str:uuid>/"),
        # This URL should exist before the detail/<str>/
        ProductContactSuccessView=(
            "contact-success",
            "contact/<str:uuid>/",
        ),
        ProductContactFormView=(
            "contact-form",
            "contact/",
        ),
        ## If 'detail' fails, the view serves 'filter'.
        ProductStockNotifyListView=(
            "stock-notify-list",
            "<str:product_id>/stock-notify-list/",
        ),
        VacgenProductDetailView=("detail", "<str:product_id>/"),
        ## Filter the product by _near_ name, returning a list of products
        VacgenProductBlankView=("detail-blank", ""),
        VacgenProductAttributeTitleListView=("productattribute-list", "attribute/"),
        VacgenProductProductAttributeValuesListView=(
            "productattribute",
            "attribute/<str:slug>/",
        ),
        VacgenProductFilterView=("filter", "filter/<str:product_id>/"),
        ImageDetail=(
            "image-detail",
            "graphic/<str:pk>/",
        ),
        ImageDetailFullSize=(
            "fullsize-image-detail",
            "graphic/<str:pk>/large/",
        ),
        BasketToGroupView=("basket-to-group", "build/group/"),
        StockNotifyFormView=(
            "stock-notify-form",
            "stock/notify/",
        ),
        StockNotifySuccessView=("stock-notify-success", "stock/notify/<str:uuid>/"),
    ),
)


class ClassPaths(trim.Paths):
    views = views

    VacgenListView = ("list", "")
    VacgenNoImageListView = ("noimage-list", "noimage/")
    ProductBrandListView = ("brands-list", "brands/")
    ProductBrandDetailView = ("brand", "brands/<str:origin_brand>/")
    # ProductAttributeListView=('productattribute-list', 'filter/')
    # AttributeTitleListView=('productattribute-list', 'filter/')
    AttributeTitleListView = ("productattribute-list", "filter/")
    AttributeTitleDetailView = ("attributetitle-detail", "filter/title/<str:pk>/")

    ProductCategoryListView = ("category-list", "category/")
    ProductCategoryDetailView = ("category", "category/<str:category_name>/")

    ## Filter the list of products within an attributevalue list,
    ## using the inherited title; e.g. spares/yes  | power/yes
    AttributeTitleValueListView = (
        "attributetitle-value-list",
        "filter/<str:title_slug>/<str:pk>/",
    )
    ProductStashListView = ("productstash-list", "stash/")
    ProductStashLabelFormView = (
        "productstash-label-form",
        "stash/form/<str:uuid>/label/",
    )
    ProductStashMergeFormView = (
        "productstash-merge-form",
        "stash/form/<str:uuid>/merge/",
    )
    ProductStashFormView = (
        "productstash-form",
        (
            "stash/form/",
            "stash/form/<str:uuid>/",
        ),
    )
    ProductStashDetailView = ("productstash-detail", "stash/<str:uuid>/")

    ProductStashDetailView = ("productstash-detail", "stash/<str:uuid>/")

    # This URL should exist before the detail/<str>/
    ProductContactSuccessView = (
        "contact-success",
        "contact/<str:uuid>/",
    )
    ProductContactFormView = (
        "contact-form",
        "contact/",
    )
    ## If 'detail' fails, the view serves 'filter'.
    ProductStockNotifyListView = (
        "stock-notify-list",
        "<str:product_id>/stock-notify-list/",
    )
    VacgenProductDetailView = ("detail", "<str:product_id>/")
    ## Filter the product by _near_ name, returning a list of products
    VacgenProductBlankView = ("detail-blank", "")
    VacgenProductAttributeTitleListView = ("productattribute-list", "attribute/")
    VacgenProductProductAttributeValuesListView = (
        "productattribute",
        "attribute/<str:slug>/",
    )
    VacgenProductFilterView = ("filter", "filter/<str:product_id>/")
    ImageDetail = (
        "image-detail",
        "graphic/<str:pk>/",
    )
    ImageDetailFullSize = (
        "fullsize-image-detail",
        "graphic/<str:pk>/large/",
    )
    BasketToGroupView = ("basket-to-group", "build/group/")

    StockNotifyFormView = (
        "stock-notify-form",
        "stock/notify/",
    )
    StockNotifySuccessView = ("stock-notify-success", "stock/notify/<str:uuid>/")
