## Trim Bundle

A 'trim bundle' binds a user friendly deployable 'package' for installation within a micro framework. For this first case django packages is the target - done correctly any developer may integrate a bundle strategy for an app.

The end-user will leverage many `company-bundler install` collecting developer sanctioned bundles, configured to _plug into_ a developers primary application.

1. The primary dev creates a bundle platform and protocol
2. primary devs and end users develop bundles and deploy to a marketplace.
3. (Other) end users install the bundle through a marketplace.
4. Clients leverage the bundle functionality.

Trim offers a range of tools to assist a primary developer with creating a custom marketplace for an application.

1. A plugin base to hook application source to bundle definitions
2. building and execution scripts for bundles
3. end-user change tracking tools

The goal is reduced complexity for an end-user when installing addons for a framework (one click installs) of primary developer sanctioned products - such as social-auth for my web app.

The integration should be agnostic to platform and wrap builtins such as setup.py zip imports to install semi-complex units automatically.

---

For the end-user (developer) they may define all the components to successfully leverage a subset of source from their eco-system.

The end-user (business) can utilise the definition to quickly implement and deploy their micro-product.

# Overview

A trim bundle should be applicable for a range of frameworks or user deployments. the core features isolate general packaging tasks, wrapping a developer preferred product. It shouldn't replace the existing infrastructure but rather leverage their correct steps, and document those step.

+ Pip for host
+ setup.py for app installation
+ python zip module import loadout for bundle directories
+ developer specific steps

A trim bundle should be manually unpackable in the event an end-user developer cannot integrate a trim packaging. If a package fails to install the root assets may unzipped and installed by hand.

## Core tools

The available components bridge one eco-system but likely integrated as discreet steps.

+ A protocol definition (the manifest)
+ bundle integration (hooks)
+ deployment (marketplace)
+ usage (install)

In all cases the `trim` provides a thin wrapper to bridge imports and installs, through a developer defines eco-system.

### Source

The primary developer has a use-case for 'plugins' and produces a definition for the end-user manifest. The primary application has source hooks to grab live modules.

TThe `trim` tools assign the API between the primary application hooks and a bundle manifest. As this is the core featureset a primary developer builds their own manifest protocol to spec, such as a "on upload" property, of which executes a script when the primary application sends the signal.

The trim signals are developer bound. In the case of django a developer may define the "onready" property will execute the `ready` module in an installed package.

### Deploy

Once an application is ready to accept bundles, the 'marketplace' of available assets provides the index of all end-user installable units.

the trim packages provide a suite of tools to present and install the finalised bundles. A UI to accept and present bundles as a 'marketplace', and script tools for the end user - offered by the primary developer.

Trim offers a set of tools to _wrap_ source into a chosen format - a "bundle builder"

+ Utilies to create a bundle - as per developer spec
+ An interface to list bundles for the end-user

### Digest

The end user installs the units through developer defines processes - in theory this is a button.

Trim provides a set of functions to _install_ the bundles within an end-user environment. In most cases this will be a case of:

+ Updating a list of installed items
+ Running an primary developer defined manifest specific "install" commands
+ Asking the user primary settings questions.

# Using trim-bundle

The use-case of a trim-bundle:

+ developing and deploying a primary host: To hoist bundles (django)
+ Integrating the trim utility: (editing settings.py with trim runtime managers)
+ Developing trim integrations: (extending trim with host hooking)
+ Building trim bundles: (Use developer defines integration for the host integration by end users)
+ Deploying a marketplace: (a ui for end users to access bundles)
+ end-user integration: (a customer of bundles using their wrapped functionality)

## primary developer

The primary developer builds and deploys the initial application, complete with the 'trim bundle' hooks and deploys the app with a sibling marketplace interface, so users may extend upon the primary exposed bundle protocol.

A primary developer defines a bundle protocol by creating their manifest definition and a method to _hook_ source within the bundle. Much of this is part of the Trim packaging so a developer may leverage existing hook patterns (such as a django module installer).

+ Builds a primary (pluginnable) framework, leveraging trim bundles
+ Defines and creates trim-bundle formats for end-user integration
+ manages a primary bundle marketplace

## The customer developer:

The customer developer are the community of users _accepting_ the primary developer content. They may be considered the _API user_ or middleman to the end-user.

The customer dev will work with the primary application through the exposed API given by the primary developer, through manifest definitions and the marketplace integration steps. Once a customer developer submits an asset to a marketplace, it can be shared through the primary developer definition (e.g. a shared ecosystem built by the primary).

+ deploy clones of the primary framework: (or has a single site host) aka: A "Secondary"
+ digests and integrates bundles
+ creates and submits bundles to the marketplace

## The end-user (Developer)

## The end-user (Business)

A end-user may be considered the 'business target' or the user to _digest_ and work with the marketplace products, and the eco-system defined by the primary developer.

In the common case, they don't work with the packaging system, except for integrating complete bundles.

## A Client

At the root and likely the most important is the 'client' or the customer of the end-user (developer or business). They only execute upon the deployed application (primary or secondary) and don't use the marketplace.

The end-user has implemented bundles to serve a client with features - such as a login system or shopping cart utility. At this point the end-user has masked the bundled product with their own branding.

In this case a client is the _person in the shop_ purchasing a t-shirt, and have no concern about the running of the shop.

+ Silently utilises the end-user experience

# Plug Packages

A "package" is a single installable unit complete with all the assets to install
a django app.

## Why not X?

This installer will leverage all the default tooling such as pip and setuptools,
but focused on installing a _micro app_ within a larger eco-system, where we can
define and leverage a distinct pattern focusing on the product.

In this case we're building django apps - with a pip, install, module, and exit tools.

### setup.py

The functionality exists here but the 'manifest' should expost a neater view for a non-coder. A 'package deploy' utility may use setup.py to build a final installable.

## package

The term 'package' and 'bundle' are interchangable. For all internal definitions a 'bundle' defines the Trim unit, a package refers to the common nomanclature used with python apps.

A trim bundle top level:
    bundle:
        manifest [yaml|json]
        docs/
        content/
        assets/
        ...

The package contains a manifest to assign downloads and installations for the
package, appended to the pip and django installation systems.

A manifest may be in a digestable transport format. My preference is YAML because
it's nice to read

---

The outer package, wrapping the 'content' is not code defined - and exists to hold all assets as one entity.
The manifest defines the important parts.

## manifest

    name: django trim
    unique: django_trim
    requirements:
        - django>=3.0
        - six
        - requests
    installed_apps:
        - trim
    ...

### requirements

The requirements is an extention of the standard pip installer, listing them to
install the package.

Within the manifest this may be a package, file or combination of both. upon package installation the user or system may opt for a 'package install'

manifest:

    requirements: pointer+identity+hash
    requirements:
        - identity+hash
        - identity+hash
    requirements:
        - identity+hash
        - pointer+identity+hash

The 'pointer' manages the internal protocol to accept the data:

+ file
+ http
+ stream
+ [undefined] package-name

An 'identity' refers to the pointer unit such as a filename or package-name

+ file+requirements.txt
+ http+intranet.foo.bar/generic.txt
+ stream:stdin

## Install

A package command manages a clean install of the unit. Generally this is a

+ _pointer_ to the installed file (a standard python module)
+ any requirements
+ Migrations

Much of the functionality exists as a single module and can be mapped into a global
space with an 'enabled'

---

For django a primary install routine is add to INSTALLED_APPS. This should occur be default with an 'enabled' switch for the package.

## Verifying

The package 'state' is verified with crc and can be verified with a CRC check or tested for new changes.

## Versioning

All trim packages should have a version. Usually the _latest_ is applied as per config of the marketplace developer.

# Primary Integration

In this example django is the primary platform, and django packages will be installed to an end-user deployment though a primary marketplace.

The trim package should be implemented into the primary platform before the bundles are installed.

    pip install trim-django

The trim hooks specific to this api should be applied to the primary platform source:

settings.py

```py
INSTALLED_APPS += trim.packages()
```

# User Integration

The end user installed packages within their secondary application through the primary developer requirements. The general cases are:

+ An 'install' button within a marketplace
+ A _local_ install within the secondary source.

In both cases the deployed application (bundle digestor) may need to restart and perform any runtime changes. The secondary application must include the primary application marketplace services. This should be applied within the secondary source by default, or as a separate integration step from the primary developer:

    Hi team, I've made a bundler for all our internal apps. First get our "company primary-app" and "pip install company-bundler". Install the company-bundler with the site instructions.
    Go to the marketplace and then install with "company-bundler install APP-NAME ..."

The end-user will leverage many `company-bundler install`, collecting developer sanctioned bundles, configured to _plug into_ a developers primary application
