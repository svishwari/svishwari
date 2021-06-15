import { Serializer } from "miragejs"

/**
 * Serializer used for the Mirage.js API
 */
export default Serializer.extend({
  embed: true,
  root: false,
  alwaysIncludeLinkageData: true,
})
