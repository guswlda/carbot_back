const express = require('express');
const router = express.Router();
const {
  makeCall,
  handleWebSocket,
} = require('../../controllers/callbot/callbotController');

// express-ws를 라우터에 적용
const expressWs = require('express-ws');
expressWs(router);

// 전화를 시작하는 엔드포인트
router.get('/make-call', (req, res) => {
  makeCall();
  res.send('Vonage call initiated');
});

// WebSocket 엔드포인트
router.ws('/ws', handleWebSocket);

module.exports = router;
