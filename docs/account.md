# Account module

The trim account module aims to simplify generic user login, offering a _login_, _logout_, _profile_ and a few associated pages. This is specificially designed to expose the standard Django user for general user accounts and not intended to replace or override the existing users.

Fundamentally `trim.account` creates those extra login pages given to standard users. The `django` admin, and `wagtail` admin login pages will still function as expected.


> [!NOTE]
> We opted for the `account` (singular) here to ensure the more generic _accounts/_ (plural) is available for your own tools.


## Install

Add to installed apps:

```py
INSTALLED_APPS = [
    'trim',
    'trim.account',   # A sub module of the trim package.
]
```

Add to settings for redirects:

```py
LOGIN_REDIRECT_URL = 'account:profile'
LOGIN_URL = 'account:login'
```

Add to URLs:

```py
from trim.urls import path_includes as includes

# path('account/', include('trim.account.urls'))
urlpatterns += includes(
        'trim.account',
        ...
    )
```

And you're good to go, head to the account login page such as  `/trim.account/login/`


- The associated model `trim.account.Account` is a _one to one_ related object, created when required. It's not required for the basic account login.

## Info

An Account contains the master reference for all single user or org to
administer access credentials, purchases and any other settings specific to
an identity.

+ OAuth cross associations
+ Company Associations
+ Purchases

---

## OAuth

A single user may sign into the application through a third part oauth provider
such as google. The same user may also login through additional third party clients.

Furhtermore a single account may be decoupled from the thirdparty - but still exist with a _real_ login. All these factor into the one user account - allowing a single identity to
login through any validated oauth.


## Org or Company

An Organisation consists of an institution and many members. An organisation needs to exist for _pricing_ and purchase verification, thus a user may be associated with a company - once valdiated by the administrator.

The user may see the purchases, prices, or other company information - given access by their admin.

> This highlights a potential loophole with the pricing method - as a user may somehow gain access to two independant organisations and see each pricing strategy.

To mitigate this, an administrator within the company should manually choose if a user can see the target pricing. In addition a notification alerts the staff of the cross reference. This is done though email assocation.

---

A company may have unique pricing, purchasing orders and conversations.

