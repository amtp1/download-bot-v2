module.exports = {
  apps: [
    {
      name: "download-bot",
      cwd: __dirname,
      script: "poetry",
      args: "run bot",
      interpreter: "none",
      autorestart: true,
      max_restarts: 10,
      min_uptime: "10s",
      watch: false,
      env: {
        PYTHONUNBUFFERED: "1",
      },
    },
  ],
};
