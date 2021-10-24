export const get_api_url = () => {
    let result = "";
    let domainWithOutGitpod = window.location.href;
    let API_PORT = 8000;
    let FRONT_END_PORT = window.location.port;
    let substrPoint = 8 + FRONT_END_PORT.toString().length;
    if(domainWithOutGitpod.substring(0, substrPoint).includes("https://3000") && domainWithOutGitpod.substring(substrPoint, domainWithOutGitpod.length).includes("gitpod.io")) {
      result = `${domainWithOutGitpod.substring(0, 8)}${API_PORT}${domainWithOutGitpod.substring(substrPoint, domainWithOutGitpod.length)}`;
    }else {
      result = `http://localhost:${API_PORT}/`;
    }
    return result;
};