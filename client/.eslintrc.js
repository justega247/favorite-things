module.exports = {
  root: true,
  "env": {
    "browser": true,
    "node": true,
    "es6": true
  },
  parserOptions: {
    sourceType: "module",
    parser: "babel-eslint"
  },
  // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
  extends: [
    "standard",
    "plugin:vue/recommended"
  ],
  // required to lint *.vue files
  plugins: ["html", "vue"]
};
