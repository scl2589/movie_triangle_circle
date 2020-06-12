const path = require('path')

module.exports = {
    module: {
      rules: [
        // ... other rules omitted
  
        // this will apply to both plain `.scss` files
        // AND `<style lang="scss">` blocks in `.vue` files
        // {
        //     test: /\.styl(us)?$/,
        //     use: [
        //       'vue-style-loader',
        //       'css-loader',
        //       'stylus-loader'
        //     ]
        //   },
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
    }
    
  }