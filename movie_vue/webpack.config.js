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
    },
    resolve: {
      alias: {
        // If using the runtime only build
        vue$: 'vue/dist/vue.runtime.esm.js' // 'vue/dist/vue.runtime.common.js' for webpack 1
        // Or if using full build of Vue (runtime + compiler)
        // vue$: 'vue/dist/vue.esm.js'      // 'vue/dist/vue.common.js' for webpack 1
      }
    }
    
  }