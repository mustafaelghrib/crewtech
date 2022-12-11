#Amazon Elastic Compute Cloud (EC2)

variable "instance_name" { type = string }
variable "instance_ami" { type = string }
variable "instance_type" { type = string }
variable "instance_volume_size" { type = number }
variable "instance_volume_type" { type = string }
variable "instance_user" { type = string }
variable "instance_scripts" { type = list(string) }
variable "instance_ssh_name" { type = string }
variable "instance_ssh_public_key" { type = string }
variable "instance_ssh_private_key" { type = string }
variable "instance_install_aws_cli_source" { type = string }
variable "instance_install_aws_cli_destination" { type = string }
variable "instance_install_aws_cli_command" { type = string }

resource "aws_key_pair" "main" {
  key_name   = var.instance_ssh_name
  public_key = var.instance_ssh_public_key
}

resource "aws_instance" "main" {
  tags          = { "Name" = var.instance_name }
  ami           = var.instance_ami
  instance_type = var.instance_type
  key_name      = aws_key_pair.main.key_name

  root_block_device {
    volume_size = var.instance_volume_size
    volume_type = var.instance_volume_type
  }

  connection {
    type        = "ssh"
    user        = var.instance_user
    host        = self.public_dns
    private_key = var.instance_ssh_private_key
  }

  provisioner "remote-exec" {
    scripts = var.instance_scripts
  }

  provisioner "file" {
    source      = var.instance_install_aws_cli_source
    destination = var.instance_install_aws_cli_destination
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x ${var.instance_install_aws_cli_destination}",
      var.instance_install_aws_cli_command,
    ]
  }

}

output "INSTANCE_USER" { value = var.instance_user }
output "INSTANCE_IP" { value = aws_instance.main.public_dns }
output "INSTANCE_SSH_CONNECT" { value = "ssh ${var.instance_user}@${aws_instance.main.public_dns}" }
