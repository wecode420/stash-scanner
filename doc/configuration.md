# Configuration Guide
You can configure almost everything using the UI. It is important you take the time to understand and configure the tool properly if you want to get the most out of it. Make sure to apply/save once you're done making changes.

## Filters
Filters are used to find the items you want. there are two types of filters:
- **Custom:** user filters, configured using the filter editor. for reference, see [filter guide](filter.md).
- **Generated:** these are generated automatically, for every item retrieved from the API a filter is generated.  
 They are read-only and cannot be removed. You can though, adjust their prices and disable/enable them. This is done in the *Prices tab*.

## General
- **League:** the league you're interested in
- **Request delay:** minimum time delay between requests to stash API
- **Scan mode**
  - Latest: start scanning from the latest data. Use this unless you're interested in historical data.
  - Continue: resume scanning from the last stopping point. if there is none, starts from the latest data
- **Growl notifications:** turn on/off notifications
- **Notification duration** - time between alerts
- **Copy message** - whether or not to copy whisper message when a match is found

## Prices
Here you can view and customize item prices and generated filters. 
Customization is done using *overrides*. Overrides follow the same format as prices. For example, to change an item's price to be 20 chaos, just put in `20 chaos`.  
overrides can be relative to the original price. Examples: `+1 ex`, `* 3`, `/ 2`, `-10 chaos`

  - **Item value threshold:** think of this as the minimum value of items you're interested in. *Generated* filters for items with effective price below this threshold will be disabled.
  - **Default item value override:** default item price override. if none is specified, this is used. Default is `* 1` which does nothing.
  - **Default filter override:** default filter price override. if none is specified, this is used. For example, by setting this to `* 0.8` you're telling the app you want to be notified when an item is posted at 80% of its value.
  - Table columns: 
    - **Item price:** item price as it was retrieved from the API
    - **Override:** use this to adjust item prices
    - **Filter price:** the effective item price (which means item price after override is applied).
    - **Filter override:** use this to adjust the generated filter price, if none is specified the default filter price override is used.
    - **Effective filter price:** filter price after override is applied
    - **Filter state override:** use this override if a specific filter is disabled because it is under the threshold and you want to enable it anyway.  
    same goes for specific filters you want disabled even though they're above the threshold

## Currency
Here you can view and customize currency rates
  - **Rate:** currency rate as retrieved from the API
  - **Override:** use this to modify the rate
  - **Effective rate:** rate after override (if any) is applied

Note the API might not provide a rate for extremely rare currency such as mirrors/eternal orbs. This can create false alerts because their rate will default to 0.
To avoid that, provide an estimated price using an override, such as `50 ex` or whatever you see fit.

## Disabling generated filters
* **By item value:** generally *generated* filters above the threshold will be active.  By settings it to a high enough value, you can disable all generated filters if you wish. You can set it in the *Prices tab*, under **item value threshold**

* **Specific:** you can control individual filters if you use set their state override in the *Prices tab*. this will force a specific filter to be disabled/enabled, ignoring other configurations.

* **By category:** you can disable filters by categories but it can't be done using the UI yet.  
to do that you need to open up *filters.config.json* and fill *disabled_categories*. Make sure the application is closed before you do. Example how this looks like:
```
{
    "default_fprice_override": "* 0.7",
    "default_price_override": "* 1",
    "disabled_categories": [
        "divinationcards",
        "essence",
        "prophecy",
        "uniqueaccessory",
        "uniquearmour",
        "uniqueflask",
        "uniquejewel",
        "uniqueweapon",
        "uniquemap"
    ],
    "filter_price_overrides": {},
    "filter_state_overrides": {},
    "price_overrides": {},
    "price_threshold": "10 chaos"
}
```

## File structure
Under `cfg` directory:
- `app.ini`: contains general setting and preferences
- `filters.json`: contains user item filters information
- `filters.config.json`: contains mostly configuration for generated filters. price threshold, item price overrides, price overrides and disabled categories
- `currency.json`: contains currency information. currency names, rates, rates overrides, etc.
