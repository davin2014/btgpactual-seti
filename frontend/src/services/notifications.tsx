import { SMTPClient } from 'emailjs';

export class EmailSendService {
  private client: SMTPClient;

  constructor() {
    this.client = new SMTPClient({
      user: 'user',
      password: 'password',
      host: 'smtp.your-email.com',
      ssl: true,
    });
  }

  sendEmail(text: string, from: string, to: string, subject: string, cc: string = ''): void {
    this.client.send(
      {
        text,
        from,
        to,
        cc,
        subject,
      },
      (err, message) => {
        console.log(err || message);
      }
    );
  }
}