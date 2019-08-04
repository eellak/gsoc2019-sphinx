import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { ApiService } from '../api.service';


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {
  url: any;
  messages: any;

  constructor(private apiService: ApiService) { }

  ngOnInit() {
  }

  getAuth() {
    this.apiService.getUrlService().subscribe((data) => {
      console.log(data);
      this.url = data;
      window.location.href = this.url
    })
  }

  getMessages() {
    this.apiService.getMessagesService().subscribe((data) => {
      console.log(data);
      this.messages = data;
    })
  }


}
