const path = require('path')

module.exports = {
    module: {
      rules: [
          {
            test: /\.s[ac]ss$/i,
            use: [
              // Creates `style` nodes from JS strings
              'style-loader',
              // Translates CSS into CommonJS
              'css-loader',
              // Compiles Sass to CSS
              'sass-loader',
            ],
          },
          
          
      ],
    },
    css: {
      loaderOptions: {
        sass: {
          includePaths: [path.resolve(__dirname, './node_modules/compass-mixins/lib')]
        }
      }
    },
    
  }