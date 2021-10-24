export const get_api_url = () => {
    let result = "";
    let domainWithOutGitpod = window.location.href;
    let API_PORT = 8000;
    let FRONT_END_PORT = 3000;
    if(domainWithOutGitpod.substring(0, 12).includes(`https://${FRONT_END_PORT}`) && domainWithOutGitpod.substring(12, domainWithOutGitpod.length).includes("gitpod.io")) {
      result = `${domainWithOutGitpod.substring(0, 8)}${API_PORT}${domainWithOutGitpod.substring(12, domainWithOutGitpod.length)}`;
    }else {
      result = `http://localhost:${API_PORT}`;
    }
    return result;
};