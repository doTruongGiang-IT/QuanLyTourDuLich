export const get_api_url = () => {
    let result = "";
    // let domainWithOutGitpod = window.location.href;
    let hostName = window.location.hostname;
    let API_PORT = 8000;
    let FRONT_END_PORT = 3000;
    let frontendPortLen = FRONT_END_PORT.toString().length
    // let substrPoint = 8 + FRONT_END_PORT.toString().length;
    if(hostName.substring(0, frontendPortLen).includes(`${FRONT_END_PORT}`) && hostName.substring(frontendPortLen).includes("gitpod.io")) {
      // result = `${domainWithOutGitpod.substring(0, 8)}${API_PORT}${domainWithOutGitpod.substring(substrPoint, domainWithOutGitpod.length)}`;
      result = `https://${API_PORT}${hostName.substring(frontendPortLen)}`;
    }else {
      result = `http://localhost:${API_PORT}`;
    }
    return result;
};