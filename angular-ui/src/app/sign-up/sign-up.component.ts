import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { DOCUMENT } from '@angular/common'

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})

export class SignUpComponent implements OnInit {
  messages: any;
  user: any;
  url: any;

  constructor(private apiService: ApiService) { }

  ngOnInit() {
  }

  getAuth() {
    this.apiService.getUrlService().subscribe((data) => {
      console.log(data);
      this.url = data;
      document.location.href = this.url;
    })
  }


  getMessages() {
    this.apiService.getMessagesService().subscribe((data) => {
      console.log(data);
      this.messages = data;
    })
  }

}
