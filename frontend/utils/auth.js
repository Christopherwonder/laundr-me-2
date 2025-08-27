import * as LocalAuthentication from 'expo-local-authentication';

export const authenticate = async () => {
  const hasHardware = await LocalAuthentication.hasHardwareAsync();
  if (!hasHardware) {
    alert('Biometric authentication is not available on this device.');
    return false;
  }

  const isEnrolled = await LocalAuthentication.isEnrolledAsync();
  if (!isEnrolled) {
    alert('No biometrics are enrolled on this device.');
    return false;
  }

  const result = await LocalAuthentication.authenticateAsync({
    promptMessage: 'Authenticate to proceed',
  });

  return result.success;
};
