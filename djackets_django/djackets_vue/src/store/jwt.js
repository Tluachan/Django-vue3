import jwt_decode from 'jwt-decode'

function getUserIdFromToken(token) {
    const decodedToken = jwt_decode(token);
    console.log('decoding', decodedToken)
    return decodedToken.user_id;
  }
  
  export default getUserIdFromToken;
  