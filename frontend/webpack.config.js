const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const ReactRefreshWebpackPlugin = require("@pmmmwh/react-refresh-webpack-plugin");

let mode = "development";
let port = process.env.PORT || process.env.port;
let target = "web";

if (process.argv[4] !== "development") {
  mode = "production";
}

console.log("!!!mode =", process.argv[4]);

const cssLoader = (extra) => {
  const loaders = [
    {
      loader: MiniCssExtractPlugin.loader,
      options: {
        filename: "[name].[contenthash].css",
      },
    },
    "css-loader",
  ];

  if (extra) {
    loaders.push(extra);
  }

  return loaders;
};

const plugins = [
  new MiniCssExtractPlugin({
    filename: mode === "production" ? "[name].[contenthash].css" : "[name].css",
  }),
  new HtmlWebpackPlugin({
    template: "./src/index.html",
  }),
];

if (process.env.SERVE) {
  plugins.push(new ReactRefreshWebpackPlugin());
}

module.exports = {
  mode,
  target,
  plugins,
  devtool: mode === "development" ? "source-map" : false,
  entry: "./src/index.tsx",

devServer: {
  port: port ?? 3001,
  open: true,
  historyApiFallback: true,
  static: "./build",
  hot: mode === "development",
  allowedHosts: "all",
  host: "0.0.0.0",

    proxy: {
    "/api/account": {
      target: "http://127.0.0.1:5000",
      changeOrigin: true,
      secure: false,
    },

    "/api": {
      target: "https://gis-eng3.esemc.nsc.ru:8443/api",
      changeOrigin: true,
      secure: false,
      pathRewrite: {
        "^/api": "",
      },
    },
  },
},

  output: {
    path: path.resolve(__dirname, "build"),
    filename: "[name].[contenthash].js",
    assetModuleFilename: "assets/[name][hash][ext][query]",
    clean: true,
    publicPath: "/",
  },

  module: {
    rules: [
      {
        test: /\.(html)$/,
        use: ["html-loader"],
      },

      {
        test: /\.css$/,
        use: cssLoader(),
        exclude: /\.module\.css$/,
      },

      {
        test: /\.s?css$/,
        oneOf: [
          {
            test: /\.module\.s?css$/,
            use: [
              MiniCssExtractPlugin.loader,
              {
                loader: "css-loader",
                options: {
                  modules: {
                    localIdentName:
                      mode === "development" ? "[name]__[local]" : "[hash]",
                  },
                },
              },
              "sass-loader",
            ],
          },
          {
            use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
          },
        ],
      },

      {
        test: /\.(png|jpe?g|gif|svg|webp|ico)$/i,
        type: mode === "production" ? "asset" : "asset/resource",
      },

      {
        test: /\.(woff2?|eot|ttf|otf)$/i,
        type: "asset/resource",
      },

      {
        test: /\.ts(x?)$/,
        use: ["ts-loader"],
        exclude: /node_modules/,
      },
    ],
  },

  resolve: {
    extensions: [
      ".js",
      ".ts",
      ".tsx",
      ".scss",
      ".module.scss",
      ".css",
      ".png",
    ],
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  ignoreWarnings: [
  {
    module: /sass-loader/,
    message: /Deprecation The legacy JS API is deprecated/,
  },
],
};