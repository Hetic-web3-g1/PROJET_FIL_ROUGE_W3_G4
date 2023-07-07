import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <div id="error-page">
      <h1>Oops!</h1>
      <p>Get Stick Bugged</p>
      <p>
        <i>{error.statusText || error.message}</i>
      </p>
      <iframe width="560" height="315" src="https://www.youtube.com/embed/M5V_IXMewl4?autoplay=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
    </div>
  );
}