import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import viteCompression from 'vite-plugin-compression'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // 环境变量
  const env = loadEnv(mode, process.cwd())
  // 生产环境判断
  const isEnvProduction = mode === 'production'
  return {
    plugins: [
      vue({
        script: {
          defineModel: true,
        }
      }),
      AutoImport({
        resolvers: [ElementPlusResolver()],
      }),
      Components({
        resolvers: [ElementPlusResolver()],
      }),
      viteCompression({
        //生成压缩包gz
        verbose: true,
        disable: false,
        threshold: 10240,
        algorithm: 'gzip',
        ext: '.gz',
      }),
    ],
    define: {
      'process.env': {}
    },
    base: '/',
    server: {
      host: '0.0.0.0',
      port: 19915,
      open: true,
      https: false,
      proxy: {
        '/api': {
          target: 'http://localhost:5000/',
          changeOrigin: true,
          rewrite: (pathStr) => pathStr.replace(new RegExp('^/api'), '')
        },
      },
    },
    
    resolve: {
      alias: {
        "@": path.resolve(__dirname, './src'),
        "@api": path.resolve(__dirname, './src/api'),
        "@assets": path.resolve(__dirname, "./src/assets"),
        "@views": path.resolve(__dirname, "./src/views"),
      }
    },
    build: {
      assetsDir: "./static",
      cssCodeSplit: true,
      minify: !isEnvProduction ? 'esbuild' : 'terser',
      terserOptions: {
        compress: {
          drop_console: isEnvProduction,
          drop_debugger: isEnvProduction
        },
        output: {
          comments: true,
        },
      },
      brotliSize: false,
      sourcemap: false,
      outDir: 'dist',
      rollupOptions: {
        input: {
          main: path.resolve(__dirname, "index.html"),
        },
        output: {
          manualChunks (id) {
            if (id.includes('node_modules')) {
              return id.toString().split('node_modules/')[1].split('/')[0].toString();
            }
          }
        },
      },
    },
  }
})
