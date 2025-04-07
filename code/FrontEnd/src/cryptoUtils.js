// cryptoUtils.js
import CryptoJS from 'crypto-js';

// 定义加密密钥
const secretKey = 'your-secure-key';

// AES 加密
export function encryptPassword(password) {
  return CryptoJS.AES.encrypt(password, secretKey).toString();
}

// AES 解密
export function decryptPassword(encryptedPassword) {
  const bytes = CryptoJS.AES.decrypt(encryptedPassword, secretKey);
  return bytes.toString(CryptoJS.enc.Utf8);  // 返回解密后的密码
}
