import $ from 'jquery'
import {chain, pick, omit, filter, defaults} from 'lodash'

import TmplListGroupItem from '../templates/list-group-item'
import {setContent, slugify, createDatasetFilters, collapseListGroup} from '../util'

export default class {
  constructor (opts) {
    const decades = this._decadesWithCount(opts.datasets, opts.params)
    const decadesMarkup = decades.map(TmplListGroupItem)
    setContent(opts.el, decadesMarkup)
    collapseListGroup(opts.el)
  }

  _decadesWithCount (datasets, params) {
    return chain(datasets)
      .groupBy('decade')
      .map(function (decadesInOrg, decade) {
        const filters = createDatasetFilters(pick(params, ['decade']))
        const filteredDatasets = filter(datasetsInOrg, filters)
        const orgSlug = slugify(decade)
        const selected = params.decade && params.decade === orgSlug
        const itemParams = selected ? omit(params, 'decade') : defaults({decade: orgSlug}, params)
        return {
          title: decade,
          url: '?' + $.param(itemParams),
          count: filteredDatasets.length,
          unfilteredCount: decadesInOrg.length,
          selected: selected
        }
      })
      .orderBy('unfilteredCount', 'desc')
      .value()
  }
}
