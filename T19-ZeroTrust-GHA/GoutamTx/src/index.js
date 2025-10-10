exports.handler = async (event) => {
  console.log("Event: ", event);
  const response = {
    statusCode: 200,
    body: JSON.stringify("Hello from Lambda deployed via GitHub Actions OIDC!"),
  };
  return response;
};
