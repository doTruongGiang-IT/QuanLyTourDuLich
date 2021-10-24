export const get_api_url = () => {
    let result = "";
    let domainWithOutGitpod = window.location.href;
    let hostName = window.location.hostname;
    let API_PORT = 8000;
    let FRONT_END_PORT = 3000;
    let substrPoint = 8 + FRONT_END_PORT.toString().length;
    if(domainWithOutGitpod.substring(0, substrPoint).includes(`https://${FRONT_END_PORT}`) && domainWithOutGitpod.substring(substrPoint, domainWithOutGitpod.length).includes("gitpod.io")) {
      // result = `${domainWithOutGitpod.substring(0, 8)}${API_PORT}${domainWithOutGitpod.substring(substrPoint, domainWithOutGitpod.length)}`;
      result = `${domainWithOutGitpod.substring(0, 8)}${API_PORT}${hostName.substring(0, FRONT_END_PORT.toString().length)}`;
    }else {
      result = `http://localhost:${API_PORT}/`;
    }
    return result;
};