import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.agicompany.nognog',
  appName: "N'OG NOG",
  webDir: 'www',
  server: {
    androidScheme: 'https'
  },
  android: {
    buildOptions: {
      keystorePath: 'nognog.keystore',
      keystoreAlias: 'nognog',
    }
  },
  ios: {
    contentInset: 'always'
  }
};

export default config;
