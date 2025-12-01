# .idx/dev.nix - Konfigurasi Server Scraper
{ pkgs, ... }: {
  
  # 1. Install Software yang dibutuhkan
  channel = "stable-23.11"; 
  packages = [
    pkgs.python3
    pkgs.python311Packages.pip
    # Wajib install Chrome & Driver untuk Selenium
    pkgs.chromium
    pkgs.chromedriver
  ];

  # 2. Pengaturan Environment
  env = {
    # Memberitahu Python dimana Chrome berada
    CHROME_BIN = "${pkgs.chromium}/bin/chromium";
    CHROMEDRIVER_PATH = "${pkgs.chromedriver}/bin/chromedriver";
  };

  idx = {
    extensions = [
      "ms-python.python"
    ];

    # 3. Setting Preview (Menjalankan Streamlit)
    previews = {
      enable = true;
      previews = {
        web = {
          # Perintah untuk menjalankan Streamlit di port yang benar
          command = ["streamlit" "run" "app.py" "--server.port" "$PORT" "--server.address" "0.0.0.0"];
          manager = "web";
        };
      };
    };

    workspace = {
      # Install library python saat project dibuat
      onCreate = {
        install-deps = "pip install -r requirements.txt";
      };
      # Install ulang saat project dibuka (jaga-jaga)
      onStart = {
        install-deps = "pip install -r requirements.txt";
      };
    };
  };
}