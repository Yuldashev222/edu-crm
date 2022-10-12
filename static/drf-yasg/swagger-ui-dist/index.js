try {
  module.exports.SwaggerUIBundle = require("./swagger-ui-bundle.js")
  module.exports.SwaggerUIStandalonePreset = require("./swagger-ui-standalone-preset.js")
} catch(e) {
  // swallow the error if there's a problem loading the static.
  // allows this module to support providing the static for browserish contexts,
  // without exploding in a Node context.
  //
  // see https://github.com/swagger-api/swagger-ui/issues/3291#issuecomment-311195388
  // for more information.
}

// `absolutePath` and `getAbsoluteFSPath` are both here because at one point,
// we documented having one and actually implemented the other.
// They were both retained so we don't break anyone's code.
module.exports.absolutePath = require("./absolute-path.js")
module.exports.getAbsoluteFSPath = require("./absolute-path.js")
