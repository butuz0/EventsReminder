import PasswordResetConfirmForm from "@/components/forms/auth/PasswordResetConfirmForm";

interface ResetPasswordPageProps {
  params: {
    uid: string;
    token: string;
  }
}


export default function ResetPasswordPage({params}: ResetPasswordPageProps) {
  const {uid, token} = params;
  
  return (
    <PasswordResetConfirmForm
      uid={uid}
      token={token}
    />
  );
}