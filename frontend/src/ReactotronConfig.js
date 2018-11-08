import Reactotron from "reactotron-react-js";
import { reactotronRedux } from "reactotron-redux";

Reactotron.configure({ name: "Khangram" })
    .use(reactotronRedux())
    .connect();

export default Reactotron;