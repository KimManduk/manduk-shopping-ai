const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("mandukDesktop", {
  appName: "만덕 Shopping AI Studio",
  version: "2.1-electron",
  platform: process.platform,
});
