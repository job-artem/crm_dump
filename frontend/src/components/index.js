import GoogleAuth from "@/components/GoogleAuth.vue";
import GoogleRegistration from "@/components/GoogleRegistration.vue";
import LoginView from "@/components/LoginView.vue";
import RegistrationView from "@/components/RegistrationView.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import LeftMenuBase from "@/components/navigation/LeftMenuBase.vue";
import LeftMenuAuth from "@/components/navigation/LeftMenuAuth.vue";
import TabAuth from "@/components/navigation/TabAuth.vue";
import TabBase from "@/components/navigation/TabBase.vue";

export default [
  GoogleRegistration, GoogleAuth, TabAuth, TabBase, LeftMenuBase, LeftMenuAuth, LoginView, RegistrationView, ProfilePage
]
