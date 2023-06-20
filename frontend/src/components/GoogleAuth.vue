<template>
    <GbUi :button-text="'Авторизация через Google'" @click="loginWithGoogle"/>
</template>
<script>
import {useTokenClient} from "vue3-google-signin";
import axios from "axios";
import GbUi from "@/components/UI/GoogleButtonUI.vue";

export default {
  components: {GbUi},
    emits: ["login-successful", "login-failed"],
    setup(_, {emit}) {
        const handleOnLogin = async ({access_token}) => {
            try {
                const response = await axios.post("login/", {token: access_token});
                emit("login-successful", response.data);
            } catch (error) {
                emit("login-failed", error);
            }
        };

        const {login} = useTokenClient({
            onSuccess: handleOnLogin,
        });

        const loginWithGoogle = async () => {
            await login();
        };

        return {
            loginWithGoogle,
        };
    },
};
</script>
<style scoped>
</style>
