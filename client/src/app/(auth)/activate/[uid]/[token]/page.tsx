import AccountActivation from "@/components/auth/AccountActivation";

interface ActivationProps {
  params: {
    uid: string;
    token: string;
  };
}


export default async function AccountActivationPage({params}: ActivationProps) {
  const {uid, token} = params; // await for async params
  return <AccountActivation uid={uid} token={token}/>;
}