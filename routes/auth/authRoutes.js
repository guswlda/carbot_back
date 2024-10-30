const router = require('express').Router();
const {
  signUp,
  customLogin,
  adminLogin,
  dealerLogin,
  customLogout,
  findId,
  emailAuth,
  verifyNumber,
  updatePassword,
  verifyUser,
} = require('../../controllers/auth/authController');

router.post('/sign_up', signUp);
router.post('/custom_login', customLogin);
router.post('/admin_login', adminLogin);
router.post('/dealer_login', dealerLogin);
router.post('/custom_logout', customLogout);
router.post('/find_id', findId);
router.post('/send_email', emailAuth);
router.post('/verify_email', verifyNumber);
router.post('/update_pass', updatePassword);
router.post('/verify_user', verifyUser);

module.exports = router;
